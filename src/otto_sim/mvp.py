"""Lightweight Otto cycle computations for the MVP pipeline."""

from __future__ import annotations

import math
from typing import Tuple


def compute_displacement_total(bore_m: float, stroke_m: float, n_cyl: int) -> Tuple[float, float]:
    """
    Compute total displacement for an engine configuration.

    Args:
        bore_m: Cylinder bore in meters.
        stroke_m: Piston stroke in meters.
        n_cyl: Number of cylinders.

    Returns:
        Tuple of (total displacement in m^3, total displacement in cm^3).
    """
    if n_cyl <= 0:
        raise ValueError("n_cyl must be positive")

    volume_per_cyl = (math.pi / 4.0) * (bore_m ** 2) * stroke_m
    total_m3 = volume_per_cyl * float(n_cyl)
    total_cm3 = total_m3 * 1.0e6
    return total_m3, total_cm3


def compute_mean_piston_speed(stroke_m: float, rpm: float) -> float:
    """
    Compute mean piston speed.

    Args:
        stroke_m: Piston stroke in meters.
        rpm: Engine speed in revolutions per minute.

    Returns:
        Mean piston speed in meters per second.
    """
    if rpm <= 0:
        raise ValueError("rpm must be positive")

    return 2.0 * stroke_m * rpm / 60.0


def compute_otto_efficiency(compression_ratio: float, k: float = 1.4) -> float:
    """
    Compute air-standard Otto efficiency.

    Args:
        compression_ratio: Compression ratio (dimensionless).
        k: Ratio of specific heats (gamma). Defaults to 1.4.

    Returns:
        Otto cycle efficiency (0..1).
    """
    if compression_ratio <= 1.0:
        raise ValueError("compression_ratio must be > 1")
    if k <= 1.0:
        raise ValueError("k must be > 1")

    return 1.0 - 1.0 / (compression_ratio ** (k - 1.0))


def compute_power_kw(torque_nm: float, rpm: float) -> float:
    """
    Estimate shaft power from torque and rpm.

    Args:
        torque_nm: Torque in Newton-meters.
        rpm: Engine speed in revolutions per minute.

    Returns:
        Power in kilowatts.
    """
    if rpm <= 0:
        raise ValueError("rpm must be positive")

    return torque_nm * (2.0 * math.pi * rpm / 60.0) / 1000.0
