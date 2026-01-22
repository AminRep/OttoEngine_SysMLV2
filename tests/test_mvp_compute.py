import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from otto_sim.mvp import (
    compute_displacement_total,
    compute_mean_piston_speed,
    compute_otto_efficiency,
    compute_power_kw,
)


def test_displacement_total():
    total_m3, total_cm3 = compute_displacement_total(0.086, 0.086, 4)
    assert math.isclose(total_m3, 0.001998228856871709, rel_tol=1e-6)
    assert math.isclose(total_cm3, 1998.228856871709, rel_tol=1e-6)


def test_mean_piston_speed():
    speed = compute_mean_piston_speed(0.086, 3000)
    assert math.isclose(speed, 8.6, rel_tol=1e-6)


def test_otto_efficiency():
    eta = compute_otto_efficiency(10.0, k=1.4)
    assert math.isclose(eta, 0.6018928294465027, rel_tol=1e-6)


def test_power_kw():
    power = compute_power_kw(200.0, 3000.0)
    assert math.isclose(power, 62.83185307179586, rel_tol=1e-6)
