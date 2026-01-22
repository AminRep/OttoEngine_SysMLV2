"""Resolve SysML parameters into canonical simulation inputs with diagnostics."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _load_parameter_map() -> Dict[str, tuple]:
    root = Path(__file__).resolve().parents[2]
    fusion_path = root / "scripts" / "fusion"
    if fusion_path.exists() and str(fusion_path) not in sys.path:
        sys.path.insert(0, str(fusion_path))

    try:
        from sysml_fusion_bridge import PARAMETER_MAP  # type: ignore
    except Exception:
        return {}

    return PARAMETER_MAP


PARAMETER_MAP = _load_parameter_map()
FUSION_TO_SYSML = {v[0].lower(): k for k, v in PARAMETER_MAP.items()}

CANONICAL_INPUTS = {
    "bore_m": {
        "direct": ["bore"],
        "aliases": ["bore_diameter", "boreDiameter", "cylinderBore", "boreDia"],
        "kind": "length",
    },
    "stroke_m": {
        "direct": ["stroke"],
        "aliases": ["stroke_length", "strokeLength"],
        "kind": "length",
    },
    "compression_ratio": {
        "direct": ["compressionRatio"],
        "aliases": ["compression_ratio", "compressionratio", "compression", "compRatio", "cr"],
        "kind": "ratio",
    },
    "n_cylinders": {
        "direct": ["numberOfCylinders"],
        "aliases": [
            "numCylinders",
            "cylinders",
            "cylinderCount",
            "cylinder_count",
            "nCylinders",
        ],
        "kind": "count",
    },
    "rpm": {
        "direct": ["rpm"],
        "aliases": ["engineSpeed", "ratedSpeed", "speed", "maxRotationalSpeed", "rotationalSpeed", "maxSpeed"],
        "kind": "speed",
    },
}

OPTIONAL_INPUTS = {
    "torque_nm": {
        "direct": ["maxTorque"],
        "aliases": ["torque", "ratedTorque", "max_torque", "torqueNm", "torque_nm"],
        "kind": "torque",
    },
    "k": {
        "direct": ["k"],
        "aliases": ["gamma", "heatCapacityRatio"],
        "kind": "ratio",
    },
}


def get_candidate_keys(canonical_key: str) -> List[str]:
    """Return candidate raw keys in match order for a canonical key."""
    entry = CANONICAL_INPUTS.get(canonical_key) or OPTIONAL_INPUTS.get(canonical_key)
    if not entry:
        return []

    candidates: List[str] = []
    direct = entry.get("direct", [])
    aliases = entry.get("aliases", [])

    for key in direct:
        if key not in candidates:
            candidates.append(key)

    for key in direct:
        if key in PARAMETER_MAP:
            fusion_name = PARAMETER_MAP[key][0]
            if fusion_name not in candidates:
                candidates.append(fusion_name)

    for key in aliases:
        if key not in candidates:
            candidates.append(key)

    return candidates


def _coerce_value(raw_value: Any) -> Tuple[Optional[float], Optional[str], str]:
    source = "raw_params"
    unit: Optional[str] = None
    value = raw_value

    if isinstance(raw_value, dict):
        value = raw_value.get("value", raw_value)
        unit = raw_value.get("unit") or raw_value.get("units")
        source = raw_value.get("source", source)

    if isinstance(value, (int, float)):
        return float(value), unit, source

    if isinstance(value, str):
        unit_match = re.search(r"\[(.*?)\]", value)
        if unit_match and not unit:
            unit = unit_match.group(1).strip()

        num_match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", value)
        if num_match:
            return float(num_match.group(0)), unit, source

    return None, unit, source


def _find_key(raw_params: Dict[str, Any], candidates: List[Tuple[str, str, Optional[str]]]) -> Optional[dict]:
    for candidate, match_type, sysml_key in candidates:
        for raw_key, raw_value in raw_params.items():
            if raw_key.lower() == candidate.lower():
                return {
                    "candidate": candidate,
                    "match_type": match_type,
                    "sysml_key": sysml_key,
                    "raw_key": raw_key,
                    "raw_value": raw_value,
                }
    return None


def _resolve_unit_hint(raw_key: str, sysml_key: Optional[str]) -> Optional[str]:
    if sysml_key and sysml_key in PARAMETER_MAP:
        return PARAMETER_MAP[sysml_key][3]

    lower_key = raw_key.lower()
    if lower_key in FUSION_TO_SYSML:
        sysml = FUSION_TO_SYSML[lower_key]
        return PARAMETER_MAP.get(sysml, (None, None, None, None))[3]

    return None


def _normalize_length(value: float, unit: Optional[str]) -> Tuple[float, Optional[str], Optional[str]]:
    conversion = None
    heuristic = None
    unit_norm = unit.lower() if unit else None

    if unit_norm in ["mm", "millimeter", "millimeters"]:
        conversion = "mm_to_m"
        return value / 1000.0, conversion, heuristic
    if unit_norm in ["cm", "centimeter", "centimeters"]:
        conversion = "cm_to_m"
        return value / 100.0, conversion, heuristic
    if unit_norm in ["m", "meter", "meters"]:
        return value, conversion, heuristic

    if value > 5:
        heuristic = "assume_mm_gt_5"
        conversion = "mm_to_m"
        return value / 1000.0, conversion, heuristic

    heuristic = "assume_m_le_5"
    return value, conversion, heuristic


def resolve_inputs(
    raw_params: Dict[str, Any],
    rpm_override: Optional[float] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    diagnostics: Dict[str, Any] = {
        "matches": {},
        "assumptions": [],
        "overrides": {},
        "missing": [],
    }

    resolved: Dict[str, Any] = {}

    for canonical_key, config in CANONICAL_INPUTS.items():
        candidates: List[Tuple[str, str, Optional[str]]] = []
        for key in config.get("direct", []):
            candidates.append((key, "direct", key))
        for key in config.get("direct", []):
            if key in PARAMETER_MAP:
                fusion_name = PARAMETER_MAP[key][0]
                candidates.append((fusion_name, "param_map", key))
        for key in config.get("aliases", []):
            candidates.append((key, "alias", None))

        match = _find_key(raw_params, candidates)
        if not match:
            diagnostics["missing"].append(canonical_key)
            continue

        raw_key = match["raw_key"]
        raw_value = match["raw_value"]
        match_type = match["match_type"]
        sysml_key = match["sysml_key"]
        value, unit, source = _coerce_value(raw_value)

        if value is None:
            diagnostics["missing"].append(canonical_key)
            continue

        unit_hint = _resolve_unit_hint(raw_key, sysml_key)
        unit = unit or unit_hint
        conversion = None
        heuristic = None
        normalized = value

        if config["kind"] == "length":
            normalized, conversion, heuristic = _normalize_length(value, unit)
        elif config["kind"] == "count":
            normalized = int(round(value))

        resolved[canonical_key] = normalized
        diagnostics["matches"][canonical_key] = {
            "source_key": raw_key,
            "source": source,
            "raw_value": raw_value,
            "parsed_value": value,
            "unit": unit,
            "normalized_value": normalized,
            "match_type": match_type,
            "unit_conversion": conversion,
            "heuristic": heuristic,
        }

        if heuristic:
            diagnostics["assumptions"].append(
                f"{canonical_key}: {heuristic} for value {value}"
            )
        if conversion:
            diagnostics["assumptions"].append(
                f"{canonical_key}: applied {conversion}"
            )

    for canonical_key, config in OPTIONAL_INPUTS.items():
        candidates: List[Tuple[str, str, Optional[str]]] = []
        for key in config.get("direct", []):
            candidates.append((key, "direct", key))
        for key in config.get("direct", []):
            if key in PARAMETER_MAP:
                fusion_name = PARAMETER_MAP[key][0]
                candidates.append((fusion_name, "param_map", key))
        for key in config.get("aliases", []):
            candidates.append((key, "alias", None))

        match = _find_key(raw_params, candidates)
        if not match:
            continue

        raw_key = match["raw_key"]
        raw_value = match["raw_value"]
        match_type = match["match_type"]
        sysml_key = match["sysml_key"]
        value, unit, source = _coerce_value(raw_value)

        if value is None:
            continue

        unit_hint = _resolve_unit_hint(raw_key, sysml_key)
        unit = unit or unit_hint
        conversion = None
        heuristic = None
        normalized = value

        resolved[canonical_key] = normalized
        diagnostics["matches"][canonical_key] = {
            "source_key": raw_key,
            "source": source,
            "raw_value": raw_value,
            "parsed_value": value,
            "unit": unit,
            "normalized_value": normalized,
            "match_type": match_type,
            "unit_conversion": conversion,
            "heuristic": heuristic,
        }

    if "rpm" not in resolved and rpm_override is not None:
        resolved["rpm"] = float(rpm_override)
        diagnostics["overrides"]["rpm"] = rpm_override
        diagnostics["matches"]["rpm"] = {
            "source_key": "--rpm",
            "source": "override",
            "raw_value": rpm_override,
            "parsed_value": float(rpm_override),
            "unit": "rpm",
            "normalized_value": float(rpm_override),
            "match_type": "override",
            "unit_conversion": None,
            "heuristic": None,
        }
        if "rpm" in diagnostics["missing"]:
            diagnostics["missing"].remove("rpm")

    return resolved, diagnostics
