# Otto Engine System Requirements

Based on the INCOSE Guide to Writing Requirements and the current Otto engine model, the following requirements have been developed. Each requirement follows the characteristics of being **Necessary, Appropriate, Unambiguous, Complete, Singular, Feasible, Verifiable, and Correct**.

## Requirements Table

| Req ID | Requirement Statement | Type | Rationale | Verification Method |
|--------|----------------------|------|-----------|---------------------|
| **REQ-OE-001** | The Otto engine shall achieve a compression ratio between 8.5 and 11.5. | Performance | Compression ratio directly affects thermal efficiency and power output. This range represents typical gasoline engine values that balance efficiency with knock resistance. | Test - Measure cylinder volume at BDC and TDC |
| **REQ-OE-002** | The Otto engine shall operate at rotational speeds up to 6500 revolutions per minute. | Performance | Maximum engine speed determines power capability and operational envelope for automotive applications. | Test - Measure crankshaft rotational frequency under load |
| **REQ-OE-003** | The piston shall complete one full stroke within 86 millimeters of travel. | Design | Stroke length defines displacement volume and is constrained by bore-to-stroke ratio for optimal combustion and mechanical stress distribution. | Inspection - Measure stroke distance in CAD model and physical prototype |
| **REQ-OE-004** | The cylinder bore diameter shall be 86 millimeters ± 0.05 millimeters. | Design | Bore diameter determines displacement and combustion chamber geometry. Tight tolerance ensures consistent compression ratio across cylinders. | Inspection - CMM measurement of manufactured cylinder |
| **REQ-OE-005** | The spark plug shall ignite the air-fuel mixture when the piston position is within 5 degrees before top dead center. | Functional | Ignition timing before TDC allows flame front propagation to peak at optimal crank angle for maximum pressure and efficiency. | Test - Measure ignition timing with engine analyzer |
| **REQ-OE-006** | The intake valve shall open when the piston is at top dead center during the intake stroke. | Functional | Valve timing synchronized with piston position ensures optimal volumetric efficiency and prevents valve-to-piston interference. | Test - Verify valve timing with degree wheel and dial indicator |
| **REQ-OE-007** | The exhaust valve shall close when the piston is at top dead center during the intake stroke. | Functional | Late exhaust valve closing captures residual exhaust momentum while preventing fresh charge escape, optimizing cylinder filling. | Test - Verify valve timing with degree wheel and dial indicator |
| **REQ-OE-008** | The connecting rod length shall be at least 1.5 times the stroke length. | Design | Rod-to-stroke ratio affects piston side loading and mechanical efficiency. Minimum 1.5:1 ratio reduces friction and wear. | Analysis - Calculate ratio from CAD dimensions |
| **REQ-OE-009** | The engine shall complete the four-stroke cycle (intake, compression, power, exhaust) in 720 degrees of crankshaft rotation. | Functional | Four-stroke thermodynamic cycle requires two complete crankshaft revolutions per cycle, fundamental to Otto engine operation. | Test - Monitor cycle completion with encoder and pressure sensor |
| **REQ-OE-010** | The Otto engine mass shall not exceed 150 kilograms for a four-cylinder configuration. | Physical | Weight constraint for automotive applications affects vehicle dynamics, fuel economy, and installation requirements. | Test - Weigh assembled engine on calibrated scale |

## Requirement Classification

### Performance Requirements
- REQ-OE-001: Compression ratio
- REQ-OE-002: Maximum rotational speed

### Functional Requirements
- REQ-OE-005: Ignition timing
- REQ-OE-006: Intake valve timing
- REQ-OE-007: Exhaust valve timing
- REQ-OE-009: Four-stroke cycle completion

### Design Requirements
- REQ-OE-003: Piston stroke
- REQ-OE-004: Cylinder bore
- REQ-OE-008: Connecting rod length ratio

### Physical Requirements
- REQ-OE-010: Engine mass

## Characteristics Compliance

All requirements have been written to comply with INCOSE characteristics:

- **C1 - Necessary**: Each requirement addresses essential Otto engine functionality
- **C2 - Appropriate**: Requirements are at the system level, not implementation-specific
- **C3 - Unambiguous**: Clear, measurable criteria with specific units
- **C4 - Complete**: All necessary information for verification included
- **C5 - Singular**: Each requirement addresses one specific aspect
- **C6 - Feasible**: All requirements achievable with current automotive technology
- **C7 - Verifiable**: Each has defined verification method (Test, Inspection, or Analysis)
- **C8 - Correct**: Requirements accurately reflect Otto engine principles
- **C9 - Conforming**: Follows standard requirement statement patterns

## Notes on Requirement Patterns

Requirements follow the INCOSE-recommended pattern:
**[System] shall [action] [object] [quantification/qualification]**

Example: "The Otto engine shall achieve a compression ratio between 8.5 and 11.5."
- System: "The Otto engine"
- Shall: Mandatory keyword
- Action: "achieve"
- Object: "a compression ratio"
- Quantification: "between 8.5 and 11.5"
