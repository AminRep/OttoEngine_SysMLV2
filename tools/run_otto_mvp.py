#!/usr/bin/env python3
"""Run the OttoEngine MVP simulation pipeline."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
FUSION_PATH = ROOT / "scripts" / "fusion"

if SRC_PATH.exists() and str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
if FUSION_PATH.exists() and str(FUSION_PATH) not in sys.path:
    sys.path.insert(0, str(FUSION_PATH))

from otto_sim.mvp import (  # noqa: E402
    compute_displacement_total,
    compute_mean_piston_speed,
    compute_otto_efficiency,
    compute_power_kw,
)
from otto_sim.parameter_map import (  # noqa: E402
    get_candidate_keys,
    resolve_inputs,
)

try:
    from sysml_fusion_bridge import DEFAULT_HOST, SysMLv2Client  # type: ignore
except Exception:
    DEFAULT_HOST = "http://localhost:8081/api/rest"
    SysMLv2Client = None  # type: ignore


REQUIRED_INPUTS = ["bore_m", "stroke_m", "compression_ratio", "n_cylinders", "rpm"]


def _git_hash() -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(ROOT),
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        return None
    return None


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _extract_part_block(text: str, part_name: str) -> Optional[str]:
    pattern = re.compile(rf"\bpart\s+{re.escape(part_name)}\b")
    lines = text.splitlines()
    in_block = False
    brace_count = 0
    block_lines = []

    for line in lines:
        if not in_block:
            if pattern.search(line):
                in_block = True
                brace_count += line.count("{") - line.count("}")
                block_lines.append(line)
            continue

        block_lines.append(line)
        brace_count += line.count("{") - line.count("}")
        if brace_count <= 0:
            break

    if not block_lines:
        return None

    return "\n".join(block_lines)


def _parse_sysml_values(text: str) -> Dict[str, Dict[str, Any]]:
    values: Dict[str, Dict[str, Any]] = {}
    pattern = re.compile(
        r"attribute\s+:>>\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>[^;]+);"
    )

    for match in pattern.finditer(text):
        name = match.group("name")
        value_text = match.group("value").strip()

        num_match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", value_text)
        if not num_match:
            continue

        value = float(num_match.group(0))
        unit_match = re.search(r"\[(.*?)\]", value_text)
        unit = unit_match.group(1).strip() if unit_match else None

        values[name] = {"value": value, "unit": unit, "source": "sysml_file"}

    return values


def _load_sysml_fallback(part_name: str, target_keys: Dict[str, None]) -> Dict[str, Dict[str, Any]]:
    sysml_path = ROOT / "models" / "ottoengine.sysml"
    if not sysml_path.exists():
        return {}

    text = sysml_path.read_text(encoding="utf-8")
    block = _extract_part_block(text, part_name)
    parsed = _parse_sysml_values(block) if block else {}
    if not parsed:
        parsed = _parse_sysml_values(text)

    filtered: Dict[str, Dict[str, Any]] = {}
    target_lower = {k.lower() for k in target_keys.keys()}
    for key, payload in parsed.items():
        if key.lower() in target_lower:
            filtered[key] = payload

    return filtered


def _load_offline_params(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "raw_params" in data:
        return data["raw_params"]
    return data if isinstance(data, dict) else {}


def _format_float(value: float) -> float:
    return float(f"{value:.6f}")


def _raw_value_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, dict):
        if not value:
            return True
        inner = value.get("value")
        if inner is None:
            return True
        if isinstance(inner, str) and not inner.strip():
            return True
    return False


def _write_report(
    path: Path,
    metadata: Dict[str, Any],
    resolved_inputs: Dict[str, Any],
    diagnostics: Dict[str, Any],
    results: Dict[str, Any],
) -> None:
    lines = [
        "# OttoEngine MVP Simulation Report",
        "",
        "## Metadata",
        f"- Timestamp: {metadata.get('timestamp')}",
        f"- Host: {metadata.get('host')}",
        f"- Project: {metadata.get('project_name')} ({metadata.get('project_id')})",
        f"- Commit: {metadata.get('commit_id')}",
        f"- Part: {metadata.get('part_name')}",
        f"- Git hash: {metadata.get('git_hash')}",
        "",
        "## Inputs (resolved)",
        "| Name | Value | Source |",
        "| --- | --- | --- |",
    ]

    for key in REQUIRED_INPUTS + ["k", "torque_nm"]:
        if key not in resolved_inputs:
            continue
        match = diagnostics.get("matches", {}).get(key, {})
        source = match.get("source", "-")
        value = resolved_inputs.get(key)
        lines.append(f"| {key} | {value} | {source} |")

    lines.extend(
        [
            "",
            "## Results",
        ]
    )

    for result_key, value in results.items():
        lines.append(f"- {result_key}: {value}")

    if diagnostics.get("assumptions"):
        lines.extend(["", "## Diagnostics", "Assumptions:"])
        for item in diagnostics["assumptions"]:
            lines.append(f"- {item}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="OttoEngine MVP simulation runner")
    parser.add_argument("--host", default=DEFAULT_HOST, help="SysML v2 API host")
    parser.add_argument("--project", default="OttoEngine", help="Project name substring")
    parser.add_argument("--part", default="fourCylinderEngine", help="Part name to extract")
    parser.add_argument("--commit", help="Commit ID override")
    parser.add_argument("--rpm", type=float, help="RPM override if not in model")
    parser.add_argument(
        "--out",
        default=str(ROOT / "outputs" / "otto_mvp"),
        help="Output directory",
    )
    parser.add_argument(
        "--offline",
        help="Path to raw params JSON to run without SysON",
    )

    args = parser.parse_args()
    output_dir = Path(args.out)

    raw_params: Dict[str, Any] = {}
    project_id = None
    project_name = None
    commit_id = None
    source_mode = "syson"

    if args.offline:
        raw_params = _load_offline_params(Path(args.offline))
        source_mode = "offline"
    else:
        if SysMLv2Client is None:
            print("[ERROR] SysMLv2Client unavailable; use --offline or check imports.")
            return 1

        client = SysMLv2Client(args.host)
        project = client.find_project_by_name(args.project)
        if not project:
            print(f"[ERROR] Project not found for name match: {args.project}")
            return 1

        project_id = project.get("@id")
        project_name = project.get("name")
        if not client.set_project(project_id):
            print(f"[ERROR] Could not set project {project_id}")
            return 1

        commit_id = client.commit_id
        if args.commit:
            commit_id = args.commit
            client.commit_id = args.commit

        raw_params = client.extract_parameters(args.part) or {}

    resolved_inputs, diagnostics = resolve_inputs(raw_params, rpm_override=args.rpm)
    missing_keys = [k for k in REQUIRED_INPUTS if k not in resolved_inputs]

    if missing_keys:
        candidate_keys = {}
        for missing in missing_keys:
            for candidate in get_candidate_keys(missing):
                candidate_keys[candidate] = None

        fallback = _load_sysml_fallback(args.part, candidate_keys)
        for key, payload in fallback.items():
            if key not in raw_params or _raw_value_missing(raw_params.get(key)):
                raw_params[key] = payload

        if fallback:
            resolved_inputs, diagnostics = resolve_inputs(raw_params, rpm_override=args.rpm)
            missing_keys = [k for k in REQUIRED_INPUTS if k not in resolved_inputs]

    if missing_keys:
        print("[ERROR] Missing required inputs:")
        for key in missing_keys:
            print(f"  - {key}")
        print("Checked SysON extraction and SysML fallback. Provide --rpm if needed.")
        return 1

    k_value = resolved_inputs.get("k", 1.4)
    displacement_m3, displacement_cm3 = compute_displacement_total(
        resolved_inputs["bore_m"],
        resolved_inputs["stroke_m"],
        int(resolved_inputs["n_cylinders"]),
    )
    mean_speed = compute_mean_piston_speed(resolved_inputs["stroke_m"], resolved_inputs["rpm"])
    otto_eta = compute_otto_efficiency(resolved_inputs["compression_ratio"], k=k_value)

    results: Dict[str, Any] = {
        "total_displacement_m3": _format_float(displacement_m3),
        "total_displacement_cm3": _format_float(displacement_cm3),
        "mean_piston_speed_m_s": _format_float(mean_speed),
        "otto_efficiency": _format_float(otto_eta),
    }

    if "torque_nm" in resolved_inputs:
        results["power_kw"] = _format_float(
            compute_power_kw(resolved_inputs["torque_nm"], resolved_inputs["rpm"])
        )

    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "host": args.host if source_mode == "syson" else None,
        "project_name": project_name,
        "project_id": project_id,
        "commit_id": commit_id,
        "part_name": args.part,
        "git_hash": _git_hash(),
        "source_mode": source_mode,
    }

    _write_json(output_dir / "inputs_raw.json", {"metadata": metadata, "raw_params": raw_params})
    _write_json(output_dir / "inputs_resolved.json", {"metadata": metadata, "inputs": resolved_inputs})
    _write_json(output_dir / "diagnostics.json", {"metadata": metadata, "diagnostics": diagnostics})
    _write_json(output_dir / "results.json", {"metadata": metadata, "results": results})
    _write_report(output_dir / "report.md", metadata, resolved_inputs, diagnostics, results)

    print(f"[OK] Wrote outputs to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
