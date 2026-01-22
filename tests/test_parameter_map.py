from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from otto_sim.parameter_map import resolve_inputs


def test_resolve_inputs_direct_keys_mm_conversion():
    raw = {
        "bore": 86,
        "stroke": 86,
        "compressionRatio": 10.5,
        "numberOfCylinders": 4,
    }
    resolved, diagnostics = resolve_inputs(raw, rpm_override=3000)

    assert resolved["bore_m"] == 0.086
    assert resolved["stroke_m"] == 0.086
    assert resolved["compression_ratio"] == 10.5
    assert resolved["n_cylinders"] == 4
    assert resolved["rpm"] == 3000
    assert diagnostics["matches"]["bore_m"]["unit_conversion"] == "mm_to_m"
    assert diagnostics["matches"]["stroke_m"]["unit_conversion"] == "mm_to_m"
    assert diagnostics["matches"]["rpm"]["source"] == "override"


def test_resolve_inputs_aliases_with_heuristics():
    raw = {
        "boreDiameter": 0.086,
        "strokeLength": 0.086,
        "compression_ratio": 10.0,
        "numberOfCylinders": 4,
        "engineSpeed": 2500,
    }
    resolved, diagnostics = resolve_inputs(raw)

    assert resolved["bore_m"] == 0.086
    assert resolved["stroke_m"] == 0.086
    assert resolved["rpm"] == 2500
    assert diagnostics["matches"]["bore_m"]["heuristic"] == "assume_m_le_5"
