# Otto Engine SysML v2 Project Review

## Summary
Built a SysML v2 model of an Otto cycle engine and a working bridge toward Fusion 360 parameter sync via the SysML v2 REST API. The project combines structure, behavior, and requirements modeling with API tooling and CAD integration scaffolding.

## Scope and Goals
- Model Otto engine structure, behavior (four-stroke cycle), and requirements in SysML v2.
- Prepare CAD integration using Fusion 360 metadata and parameter mappings.
- Prototype SysML v2 API connectivity, data extraction, and upload workflows.

## Key Work Completed
- Authored the core SysML v2 model in `ottoengine.sysml` with engine parts, enums, constraints, and two example instances (four- and one-cylinder engines).
- Defined 10 formal requirements (REQ-OE-001 to REQ-OE-010) plus a requirements table aligned to INCOSE guidance.
- Added FusionLink and FusionParameter metadata to map SysML attributes to Fusion 360 parameters and sync directions.
- Implemented a SysML v2 API client and parameter extraction flow in `sysml_fusion_bridge.py`, including Fusion script generation.
- Built a Fusion 360 add-in skeleton (`OttoEngineSysMLBridge`) with Sync From SysML and Sync To SysML commands and JSON configuration.
- Documented the Otto cycle behavior with Mermaid state diagrams and a detailed narrative description.
- Created upload and diagnostics scripts/notebooks for SysML v2 API usage (project creation, commit attempts, endpoint discovery).

## Notable Outputs
- Auto-generated Fusion 360 script for `fourCylinderEngine` parameters: `fusion_script_fourCylinderEngine.py`.
- Docker Compose setup for SysON (SysML v2 API) testing.
- Multiple guides and troubleshooting notes for API upload and Fusion add-in setup.

## Tech and Tools
SysML v2, SysML v2 REST API (SysON), Python (requests), Fusion 360 API, Docker Compose, Mermaid.

## Result
Delivered a working SysML v2 Otto engine model and a practical integration path to CAD parameters, demonstrating a digital thread from model semantics to CAD values.
