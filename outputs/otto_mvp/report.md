# OttoEngine MVP Simulation Report

## Metadata
- Timestamp: 2026-01-22T16:52:06.327204+00:00
- Host: http://localhost:8081/api/rest
- Project: OttoEngine (cecfd7a6-4c86-4366-8307-fbabfe2aa30e)
- Commit: cecfd7a6-4c86-4366-8307-fbabfe2aa30e
- Part: fourCylinderEngine
- Git hash: 9c495d7

## Inputs (resolved)
| Name | Value | Source |
| --- | --- | --- |
| bore_m | 0.08 | raw_params |
| stroke_m | 0.086 | raw_params |
| compression_ratio | 10.5 | sysml_file |
| n_cylinders | 4 | raw_params |
| rpm | 3000.0 | override |
| torque_nm | 200.0 | raw_params |

## Results
- total_displacement_m3: 0.001729
- total_displacement_cm3: 1729.132597
- mean_piston_speed_m_s: 8.6
- otto_efficiency: 0.609587
- power_kw: 62.831853

## Diagnostics
Assumptions:
- bore_m: applied mm_to_m
- stroke_m: applied mm_to_m
