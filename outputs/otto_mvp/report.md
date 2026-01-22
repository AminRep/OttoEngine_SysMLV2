# OttoEngine MVP Simulation Report

## Metadata
- Timestamp: 2026-01-22T16:27:14.370839+00:00
- Host: None
- Project: None (None)
- Commit: None
- Part: fourCylinderEngine
- Git hash: 9445164

## Inputs (resolved)
| Name | Value | Source |
| --- | --- | --- |
| bore_m | 0.086 | raw_params |
| stroke_m | 0.086 | raw_params |
| compression_ratio | 10.5 | raw_params |
| n_cylinders | 4 | raw_params |
| rpm | 3000.0 | raw_params |
| torque_nm | 200.0 | raw_params |

## Results
- total_displacement_m3: 0.001998
- total_displacement_cm3: 1998.228857
- mean_piston_speed_m_s: 8.6
- otto_efficiency: 0.609587
- power_kw: 62.831853

## Diagnostics
Assumptions:
- bore_m: applied mm_to_m
- stroke_m: applied mm_to_m
