/**
 * SysML v2 Model: Otto Engine (Otto Engine)
 * Enhanced with Fusion 360 Integration Placeholders
 *
 * PURPOSE: Learn the API now, connect to Fusion later!
 *
 * Status:
 * - SysML Model - COMPLETE
 * - CAD Metadata - PLACEHOLDER (ready for Fusion)
 * - Fusion Files - TO BE CREATED LATER
 */

package OttoEngine {

    private import ISQ::*;
    private import SI::*;
    private import ScalarValues::*;
    private import Time::*;

    // ========================================
    // FUSION 360 INTEGRATION METADATA
    // (Sticky notes for future CAD connection)
    // ========================================

    metadata def FusionLink {
        doc /* Links a SysML element to a Fusion 360 artifact.
             * Fill in the real values when you create the CAD files! */

        attribute fusionProjectName : String;   // Your Fusion project name
        attribute fusionComponentName : String; // Component name in Fusion
        attribute fusionFileName : String;      // The .f3d file name
        attribute status : String;              // "placeholder" or "connected"
    }

    metadata def FusionParameter {
        doc /* Maps a SysML attribute to a Fusion 360 parameter */

        attribute fusionParamName : String;     // Parameter name in Fusion
        attribute parameterType : String;       // "dimension", "mass", "material"
        attribute syncDirection : String;       // "toFusion", "fromFusion", "both"
    }

    // ========================================
    // Enumerations
    // ========================================

    enum def FuelType {
        Gasoline;
        PremiumGasoline;
        E10;
        E85;
    }

    enum def ValveState {
        open;
        closed;
    }

    enum def PistonPosition {
        TDC;  // Top Dead Center
        BDC;  // Bottom Dead Center
    }

    // ========================================
    // COMPONENTS WITH FUSION PLACEHOLDERS
    // ========================================

    part def Piston {
        doc /* The Piston
             * Fusion Status: PLACEHOLDER - Create piston.f3d later */

        // Fusion Link (placeholder for now!)
        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "Piston_v1";
            fusionFileName = "piston.f3d";              // CREATE THIS LATER!
            status = "placeholder";                      // Change to "connected" later
        }

        attribute mass :> ISQ::mass {
            @FusionParameter {
                fusionParamName = "piston_mass";
                parameterType = "mass";
                syncDirection = "fromFusion";           // Fusion calculates mass
            }
        }

        attribute diameter :> ISQ::length {
            @FusionParameter {
                fusionParamName = "piston_diameter";
                parameterType = "dimension";
                syncDirection = "toFusion";             // SysML is the boss here
            }
        }

        attribute height :> ISQ::length {
            @FusionParameter {
                fusionParamName = "piston_height";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute pinDiameter :> ISQ::length {
            @FusionParameter {
                fusionParamName = "pin_diameter";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute position :> ISQ::length;
        ref part connectingRod : ConnectingRod;
    }

    part def Cylinder {
        doc /* The Cylinder
             * Fusion Status: PLACEHOLDER */

        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "Cylinder_v1";
            fusionFileName = "cylinder.f3d";
            status = "placeholder";
        }

        attribute mass :> ISQ::mass;

        attribute bore :> ISQ::length {
            @FusionParameter {
                fusionParamName = "bore_diameter";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute stroke :> ISQ::length {
            @FusionParameter {
                fusionParamName = "stroke_length";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute displacement :> ISQ::volume {
            @FusionParameter {
                fusionParamName = "displacement";
                parameterType = "dimension";
                syncDirection = "fromFusion";           // Fusion calculates this
            }
        }

        attribute compressionRatio : Real;

        part piston : Piston[1];
        part intakeValve : IntakeValve[1..2];
        part exhaustValve : ExhaustValve[1..2];
        part sparkPlug : SparkPlug[1];
    }

    part def ConnectingRod {
        doc /* The Connecting Rod
             * Fusion Status: PLACEHOLDER */

        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "ConnectingRod_v1";
            fusionFileName = "connecting_rod.f3d";
            status = "placeholder";
        }

        attribute mass :> ISQ::mass {
            @FusionParameter {
                fusionParamName = "conrod_mass";
                parameterType = "mass";
                syncDirection = "fromFusion";
            }
        }

        attribute length :> ISQ::length {
            @FusionParameter {
                fusionParamName = "conrod_length";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute smallEndDiameter :> ISQ::length {
            @FusionParameter {
                fusionParamName = "small_end_dia";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute bigEndDiameter :> ISQ::length {
            @FusionParameter {
                fusionParamName = "big_end_dia";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }
    }

    part def Crankshaft {
        doc /* The Crankshaft
             * Fusion Status: PLACEHOLDER */

        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "Crankshaft_v1";
            fusionFileName = "c.f3d";
            status = "placeholder";
        }

        attribute mass :> ISQ::mass {
            @FusionParameter {
                fusionParamName = "crank_mass";
                parameterType = "mass";
                syncDirection = "fromFusion";
            }
        }

        attribute length :> ISQ::length {
            @FusionParameter {
                fusionParamName = "crank_length";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute crankpinDiameter :> ISQ::length;
        attribute mainBearingDiameter :> ISQ::length;

        attribute crankRadius :> ISQ::length {
            @FusionParameter {
                fusionParamName = "crank_radius";
                parameterType = "dimension";
                syncDirection = "toFusion";
            }
        }

        attribute rotationalSpeed :> ISQ::rotationalFrequency;
        attribute torque :> ISQ::torque;
    }

    part def Valve {
        attribute mass :> ISQ::mass;
        attribute headDiameter :> ISQ::length;
        attribute stemDiameter :> ISQ::length;
        attribute lift :> ISQ::length;
        attribute valveState : ValveState;
    }

    part def IntakeValve :> Valve {
        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "IntakeValve_v1";
            fusionFileName = "intake_valve.f3d";
            status = "placeholder";
        }
    }

    part def ExhaustValve :> Valve {
        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "ExhaustValve_v1";
            fusionFileName = "exhaust_valve.f3d";
            status = "placeholder";
        }
    }

    part def SparkPlug {
        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "SparkPlug_v1";
            fusionFileName = "spark_plug.f3d";
            status = "placeholder";
        }

        attribute mass :> ISQ::mass;
        attribute threadSize :> ISQ::length;
        attribute electrodeGap :> ISQ::length;
        attribute heatRange : Integer;
    }

    // ========================================
    // MAIN DEFINITION: Otto Engine
    // ========================================

    part def OttoEngine {
        doc /* Complete Otto Engine Assembly
             * Fusion Status: PLACEHOLDER - Main assembly */

        @FusionLink {
            fusionProjectName = "OttoEngine_Project";
            fusionComponentName = "OttoEngine_Assembly";
            fusionFileName = "otto_engine_assembly.f3d";
            status = "placeholder";
        }

        attribute mass :> ISQ::mass;
        attribute totalDisplacement :> ISQ::volume;
        attribute ratedPower :> ISQ::power;
        attribute maxTorque :> ISQ::torque;
        attribute maxRotationalSpeed :> ISQ::rotationalFrequency;
        attribute numberOfCylinders : Integer;
        attribute fuel : FuelType;

        part cylinder : Cylinder[4..12];
        part crankshaft : Crankshaft[1];
        part connectingRods : ConnectingRod[4..12];
    }

    // ========================================
    // REQUIREMENTS
    // ========================================

    // Verification method enumeration
    enum def VerificationMethod {
        Test;
        Inspection;
        Analysis;
        Demonstration;
    }

    // Requirement type classification
    enum def RequirementType {
        Performance;
        Functional;
        Design;
        Physical;
    }

    // Base requirement definition for Otto Engine
    requirement def OttoEngineRequirement {
        doc /* Base requirement for Otto Engine system */

        attribute reqType : RequirementType;
        attribute verificationMethod : VerificationMethod;
        attribute rationale : String;
    }

    // Performance Requirements
    requirement def CompressionRatioRequirement :> OttoEngineRequirement {
        doc /* The Otto engine shall achieve a compression ratio within specified limits */

        subject engine : OttoEngine;
        attribute minCompressionRatio : Real;
        attribute maxCompressionRatio : Real;
        attribute :>> reqType = RequirementType::Performance;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Compression ratio directly affects thermal efficiency and power output";
    }

    requirement def MaxRotationalSpeedRequirement :> OttoEngineRequirement {
        doc /* The Otto engine shall operate at rotational speeds up to a specified maximum */

        subject engine : OttoEngine;
        attribute maxSpeed :> ISQ::rotationalFrequency;
        attribute :>> reqType = RequirementType::Performance;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Maximum engine speed determines power capability and operational envelope";
    }

    // Design Requirements
    requirement def PistonStrokeRequirement :> OttoEngineRequirement {
        doc /* The piston shall complete one full stroke within specified travel distance */

        subject cylinder : Cylinder;
        attribute strokeLength :> ISQ::length;
        attribute :>> reqType = RequirementType::Design;
        attribute :>> verificationMethod = VerificationMethod::Inspection;
        attribute :>> rationale = "Stroke length defines displacement volume and is constrained by bore-to-stroke ratio";
    }

    requirement def CylinderBoreRequirement :> OttoEngineRequirement {
        doc /* The cylinder bore diameter shall be within specified tolerance */

        subject cylinder : Cylinder;
        attribute boreDiameter :> ISQ::length;
        attribute tolerance :> ISQ::length;
        attribute :>> reqType = RequirementType::Design;
        attribute :>> verificationMethod = VerificationMethod::Inspection;
        attribute :>> rationale = "Bore diameter determines displacement and combustion chamber geometry";
    }

    requirement def ConnectingRodRatioRequirement :> OttoEngineRequirement {
        doc /* The connecting rod length shall be at least a specified ratio of stroke length */

        subject rod : ConnectingRod;
        attribute cylinderStroke :> ISQ::length;
        attribute minRodToStrokeRatio : Real;
        attribute :>> reqType = RequirementType::Design;
        attribute :>> verificationMethod = VerificationMethod::Analysis;
        attribute :>> rationale = "Rod-to-stroke ratio affects piston side loading and mechanical efficiency";

        require constraint {
            rod.length >= minRodToStrokeRatio * cylinderStroke
        }
    }

    // Functional Requirements
    requirement def IgnitionTimingRequirement :> OttoEngineRequirement {
        doc /* The spark plug shall ignite the air-fuel mixture at specified timing before TDC */

        subject sparkPlug : SparkPlug;
        attribute timingBeforeTDC :> ISQ::planeAngle;
        attribute :>> reqType = RequirementType::Functional;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Ignition timing allows flame front propagation to peak at optimal crank angle";
    }

    requirement def IntakeValveTimingRequirement :> OttoEngineRequirement {
        doc /* The intake valve shall open when the piston is at TDC during intake stroke */

        subject valve : IntakeValve;
        attribute pistonPos : PistonPosition;
        attribute :>> reqType = RequirementType::Functional;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Valve timing synchronized with piston position ensures optimal volumetric efficiency";
    }

    requirement def ExhaustValveTimingRequirement :> OttoEngineRequirement {
        doc /* The exhaust valve shall close when the piston is at TDC during intake stroke */

        subject valve : ExhaustValve;
        attribute pistonPos : PistonPosition;
        attribute :>> reqType = RequirementType::Functional;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Late exhaust valve closing captures residual exhaust momentum while preventing fresh charge escape";
    }

    requirement def FourStrokeCycleRequirement :> OttoEngineRequirement {
        doc /* The engine shall complete the four-stroke cycle in 720 degrees of crankshaft rotation */

        subject engine : OttoEngine;
        attribute cycleRotation :> ISQ::planeAngle;
        attribute :>> reqType = RequirementType::Functional;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Four-stroke thermodynamic cycle requires two complete crankshaft revolutions per cycle";

        require constraint {
            cycleRotation == 4.0 * 3.14159265359 [rad]
        }
    }

    // Physical Requirements
    requirement def EngineMassRequirement :> OttoEngineRequirement {
        doc /* The Otto engine mass shall not exceed specified limit for given configuration */

        subject engine : OttoEngine;
        attribute maxMass :> ISQ::mass;
        attribute cylinderConfig : Integer;
        attribute :>> reqType = RequirementType::Physical;
        attribute :>> verificationMethod = VerificationMethod::Test;
        attribute :>> rationale = "Weight constraint affects vehicle dynamics, fuel economy, and installation requirements";

        require constraint {
            engine.mass <= maxMass
        }
    }

    // ========================================
    // OTTO ENGINE REQUIREMENT SPECIFICATION
    // ========================================

    requirement ottoEngineSpecification {
        doc /* Complete requirements specification for Otto Engine system */

        requirement <'REQ-OE-001'> compressionRatioReq : CompressionRatioRequirement {
            doc /* The Otto engine shall achieve a compression ratio between 8.5 and 11.5 */
            attribute :>> minCompressionRatio = 8.5;
            attribute :>> maxCompressionRatio = 11.5;
        }

        requirement <'REQ-OE-002'> maxRotationalSpeedReq : MaxRotationalSpeedRequirement {
            doc /* The Otto engine shall operate at rotational speeds up to 6500 RPM */
            attribute :>> maxSpeed = 680.678 [rad/s];
        }

        requirement <'REQ-OE-003'> pistonStrokeReq : PistonStrokeRequirement {
            doc /* The piston shall complete one full stroke within 86 millimeters of travel */
            attribute :>> strokeLength = 86 [mm];
        }

        requirement <'REQ-OE-004'> cylinderBoreReq : CylinderBoreRequirement {
            doc /* The cylinder bore diameter shall be 86 millimeters ± 0.05 millimeters */
            attribute :>> boreDiameter = 86 [mm];
            attribute :>> tolerance = 0.05 [mm];
        }

        requirement <'REQ-OE-005'> ignitionTimingReq : IgnitionTimingRequirement {
            doc /* The spark plug shall ignite the air-fuel mixture within 5 degrees before TDC */
            attribute :>> timingBeforeTDC = 0.0872664626 [rad];
        }

        requirement <'REQ-OE-006'> intakeValveTimingReq : IntakeValveTimingRequirement {
            doc /* The intake valve shall open when the piston is at TDC during intake stroke */
            attribute :>> pistonPos = PistonPosition::TDC;
        }

        requirement <'REQ-OE-007'> exhaustValveTimingReq : ExhaustValveTimingRequirement {
            doc /* The exhaust valve shall close when the piston is at TDC during intake stroke */
            attribute :>> pistonPos = PistonPosition::TDC;
        }

        requirement <'REQ-OE-008'> connectingRodRatioReq : ConnectingRodRatioRequirement {
            doc /* The connecting rod length shall be at least 1.5 times the stroke length */
            attribute :>> minRodToStrokeRatio = 1.5;
        }

        requirement <'REQ-OE-009'> fourStrokeCycleReq : FourStrokeCycleRequirement {
            doc /* The engine shall complete the four-stroke cycle in 720 degrees of crankshaft rotation */
            attribute :>> cycleRotation = 4.0 * 3.14159265359 [rad];
        }

        requirement <'REQ-OE-010'> engineMassReq : EngineMassRequirement {
            doc /* The Otto engine mass shall not exceed 150 kilograms for a four-cylinder configuration */
            attribute :>> maxMass = 150 [kg];
            attribute :>> cylinderConfig = 4;
        }
    }

    // ========================================
    // EXAMPLE INSTANCE: 4-Cylinder Engine
    // ========================================

    part fourCylinderEngine : OttoEngine {
        doc /* 4-Cylinder Engine Instance
             * These are the VALUES that will sync to Fusion! */

        attribute :>> mass = 120 [kg];
        attribute :>> totalDisplacement = 1.998 [L];
        attribute :>> ratedPower = 110 [kW];
        attribute :>> maxTorque = 200 [N*m];
        attribute :>> numberOfCylinders = 4;
        attribute :>> fuel = FuelType::PremiumGasoline;

        part redefines cylinder[4] {
            attribute :>> bore = 86 [mm];
            attribute :>> stroke = 86 [mm];
            attribute :>> compressionRatio = 10.5;

            part redefines piston {
                attribute :>> mass = 0.35 [kg];
                attribute :>> diameter = 85.96 [mm];
            }

            part redefines intakeValve[2] {
                attribute :>> headDiameter = 35 [mm];
            }

            part redefines exhaustValve[2] {
                attribute :>> headDiameter = 30 [mm];
            }

            part redefines sparkPlug {
                attribute :>> threadSize = 14 [mm];
                attribute :>> electrodeGap = 0.9 [mm];
            }
        }

        part redefines crankshaft {
            attribute :>> mass = 18 [kg];
            attribute :>> crankRadius = 43 [mm];
        }

        part redefines connectingRods[4] {
            attribute :>> mass = 0.55 [kg];
            attribute :>> length = 144 [mm];
        }
    }

    // ========================================
    // EXAMPLE INSTANCE: 1-Cylinder Engine
    // ========================================

    part oneCylinderEngine : OttoEngine {
        doc /* 1-Cylinder Engine Instance
             * Single cylinder configuration for smaller applications */

        attribute :>> mass = 35 [kg];
        attribute :>> totalDisplacement = 0.500 [L];
        attribute :>> ratedPower = 28 [kW];
        attribute :>> maxTorque = 50 [N*m];
        attribute :>> numberOfCylinders = 1;
        attribute :>> fuel = FuelType::Gasoline;

        part redefines cylinder[1] {
            attribute :>> bore = 86 [mm];
            attribute :>> stroke = 86 [mm];
            attribute :>> compressionRatio = 10.5;

            part redefines piston {
                attribute :>> mass = 0.35 [kg];
                attribute :>> diameter = 85.96 [mm];
            }

            part redefines intakeValve[2] {
                attribute :>> headDiameter = 35 [mm];
            }

            part redefines exhaustValve[2] {
                attribute :>> headDiameter = 30 [mm];
            }

            part redefines sparkPlug {
                attribute :>> threadSize = 14 [mm];
                attribute :>> electrodeGap = 0.9 [mm];
            }
        }

        part redefines crankshaft {
            attribute :>> mass = 8 [kg];
            attribute :>> crankRadius = 43 [mm];
        }

        part redefines connectingRods[1] {
            attribute :>> mass = 0.55 [kg];
            attribute :>> length = 144 [mm];
        }
    }

    // ========================================
    // REQUIREMENT SATISFACTION
    // ========================================

    // Satisfy requirements with four-cylinder engine design
    satisfy ottoEngineSpecification by fourCylinderEngine;

    // Satisfy requirements with one-cylinder engine design
    satisfy ottoEngineSpecification by oneCylinderEngine;
}
