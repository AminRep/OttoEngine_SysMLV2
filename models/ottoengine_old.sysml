/* *
 * SysML v2 Model: Otto Engine (Otto Engine)
 * Enhanced with Fusion 360 Integration Placeholders
 *
 * PURPOSE: Learn the API now, connect to Fusion later!
 *
 * Status:
 * - SysML Model - COMPLETE
 * - CAD Metadata - PLACEHOLDER (ready for Fusion)
 * - Fusion Files - TO BE CREATED LATER */
package OttoEngine {
	private import ISQ::*;
	private import SI::*;
	private import ScalarValues::*;
	private import Time::*;
	metadata def FusionLink {
		doc /* Links a SysML element to a Fusion 360 artifact.
		             * Fill in the real values when you create the CAD files! */
		attribute fusionProjectName : String;
		attribute fusionComponentName : String;
		attribute fusionFileName : String;
		attribute status : String;
	}
	metadata def FusionParameter {
		doc /* Maps a SysML attribute to a Fusion 360 parameter */
		attribute fusionParamName : String;
		attribute parameterType : String;
		attribute syncDirection : String;
	}
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
		TDC;
		BDC;
	}
	#FusionLink part def Piston {
		doc /* The Piston
		             * Fusion Status: PLACEHOLDER - Create piston.f3d later */
		#FusionParameter attribute mass :> ISQBase::mass;
		#FusionParameter attribute diameter :> length;
		#FusionParameter attribute height :> length;
		#FusionParameter attribute pinDiameter :> length;
		attribute position :> length;
		ref part connectingRod : ConnectingRod;
	}
	#FusionLink part def Cylinder {
		doc /* The Cylinder
		             * Fusion Status: PLACEHOLDER */
		attribute mass :> ISQBase::mass;
		#FusionParameter attribute bore :> length;
		#FusionParameter attribute stroke :> length;
		#FusionParameter attribute displacement :> volume;
		attribute compressionRatio : Real;
		part piston : Piston [1];
		part intakeValve : IntakeValve [1..2];
		part exhaustValve : ExhaustValve [1..2];
		part sparkPlug : SparkPlug [1];
	}
	#FusionLink part def ConnectingRod {
		doc /* The Connecting Rod
		             * Fusion Status: PLACEHOLDER */
		#FusionParameter attribute mass :> ISQBase::mass;
		#FusionParameter attribute length :> ISQBase::length;
		#FusionParameter attribute smallEndDiameter :> ISQBase::length;
		#FusionParameter attribute bigEndDiameter :> ISQBase::length;
	}
	#FusionLink part def Crankshaft {
		doc /* The Crankshaft
		             * Fusion Status: PLACEHOLDER */
		#FusionParameter attribute mass :> ISQBase::mass;
		#FusionParameter attribute length :> ISQBase::length;
		attribute crankpinDiameter :> ISQBase::length;
		attribute mainBearingDiameter :> ISQBase::length;
		#FusionParameter attribute crankRadius :> ISQBase::length;
		attribute rotationalSpeed :> rotationalFrequency;
		attribute torque :> ISQMechanics::torque;
	}
	part def Valve {
		attribute mass :> ISQBase::mass;
		attribute headDiameter :> length;
		attribute stemDiameter :> length;
		attribute lift :> length;
		attribute valveState : ValveState;
	}
	#FusionLink part def IntakeValve :> Valve;
	#FusionLink part def ExhaustValve :> Valve;
	#FusionLink part def SparkPlug {
		attribute mass :> ISQBase::mass;
		attribute threadSize :> length;
		attribute electrodeGap :> length;
		attribute heatRange : Integer;
	}
	#FusionLink part def OttoEngine {
		doc /* Complete Otto Engine Assembly
		             * Fusion Status: PLACEHOLDER - Main assembly */
		attribute mass :> ISQBase::mass;
		attribute totalDisplacement :> volume;
		attribute ratedPower :> power;
		attribute maxTorque :> torque;
		attribute maxRotationalSpeed :> rotationalFrequency;
		attribute numberOfCylinders : Integer;
		attribute fuel : FuelType;
		part cylinder : Cylinder [4..12];
		part crankshaft : Crankshaft [1];
		part connectingRods : ConnectingRod [4..12];
	}
	part fourCylinderEngine : OttoEngine {
		doc /* 4-Cylinder Engine Instance
		             * These are the VALUES that will sync to Fusion! */
		attribute :>> mass = 120 [kg];
		attribute :>> totalDisplacement = 2.0 [L];
		attribute :>> ratedPower = 110 [kW];
		attribute :>> maxTorque = 200 [N * m];
		attribute :>> numberOfCylinders = 4;
		attribute :>> fuel = PremiumGasoline;
		part :>> cylinder [4] {
			attribute :>> bore = 86 [mm];
			attribute :>> stroke = 86 [mm];
			attribute :>> compressionRatio = 10.5;
			part :>> piston {
				attribute :>> mass = 0.35 [kg];
				attribute :>> diameter = 85.96 [mm];
			}
			part :>> intakeValve [2] {
				attribute :>> headDiameter = 35 [mm];
			}
			part :>> exhaustValve [2] {
				attribute :>> headDiameter = 30 [mm];
			}
			part :>> sparkPlug {
				attribute :>> threadSize = 14 [mm];
				attribute :>> electrodeGap = 0.9 [mm];
			}
		}
		part :>> crankshaft {
			attribute :>> mass = 18 [kg];
			attribute :>> crankRadius = 43 [mm];
		}
		part :>> connectingRods [4] {
			attribute :>> mass = 0.55 [kg];
			attribute :>> length = 144 [mm];
		}
	}
	part oneCylinderEngine : OttoEngine {
		doc /* 1-Cylinder Engine Instance
		             * Single cylinder configuration for smaller applications */
		attribute :>> mass = 35 [kg];
		attribute :>> totalDisplacement = 0.5 [L];
		attribute :>> ratedPower = 28 [kW];
		attribute :>> maxTorque = 50 [N * m];
		attribute :>> numberOfCylinders = 1;
		attribute :>> fuel = Gasoline;
		part :>> cylinder [1] {
			attribute :>> bore = 97 [mm];
			attribute :>> stroke = 86 [mm];
			attribute :>> compressionRatio = 10.5;
			part :>> piston {
				attribute :>> mass = 0.35 [kg];
				attribute :>> diameter = 85.96 [mm];
			}
			part :>> intakeValve [2] {
				attribute :>> headDiameter = 35 [mm];
			}
			part :>> exhaustValve [2] {
				attribute :>> headDiameter = 30 [mm];
			}
			part :>> sparkPlug {
				attribute :>> threadSize = 14 [mm];
				attribute :>> electrodeGap = 0.9 [mm];
			}
			view view1 : StandardViewDefinitions::GeneralView {
				expose OttoEngine::oneCylinderEngine::cylinder;
				expose OttoEngine;
				expose Cylinder;
			}
		}
		part :>> crankshaft {
			attribute :>> mass = 8 [kg];
			attribute :>> crankRadius = 32 [mm];
		}
		part :>> connectingRods [1] {
			attribute :>> mass = 0.55 [kg];
			attribute :>> length = 148 [mm];
		}
	}
}