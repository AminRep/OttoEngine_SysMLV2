# Otto Engine SysML v2 Project

A SysML v2 model of an Otto cycle engine with requirements and behavior, plus tooling to sync model parameters with Autodesk Fusion 360 through the SysML v2 API (SysON).

## What is here
- `models/ottoengine.sysml`: core SysML v2 model (structure, enums, constraints, and instances).
- `docs/model/otto_engine_requirements_table.md`: requirements table (REQ-OE-001 through REQ-OE-010).
- `docs/model/stateDiagram_Ottomotor.md` and `docs/model/ottoZyklus_Beschreibung.md`: behavior documentation for the four-stroke cycle.
- `scripts/fusion/sysml_fusion_bridge.py`: SysML v2 API client and parameter extraction plus Fusion 360 script generator.
- `bridge/OttoEngineSysMLBridge/`: Fusion 360 add-in for sync to and from SysML.
- `scripts/api/`: SysON API helper scripts and upload guidance.
- `infra/docker-compose.yml`: local SysON stack for testing.
- `cad/` and `assets/`: CAD assets and reference images.
- `notebooks/workspace.ipynb`: exploration notebook.

## Quick start
### 1) Run a local SysML v2 API (SysON)
```bash
cd infra
docker-compose up -d
```
This exposes the API at `http://localhost:8081/api/rest` (adjust hosts in scripts or configs if needed).

### 2) Inspect the model
Open `models/ottoengine.sysml`. It includes metadata for Fusion parameter mapping.

### 3) Extract parameters or generate a Fusion 360 script
```bash
python scripts/fusion/sysml_fusion_bridge.py --list-projects
python scripts/fusion/sysml_fusion_bridge.py --extract fourCylinderEngine --generate-fusion-script
```
The generated script is written next to the bridge script as `fusion_script_<part>.py`.

### 4) Use the Fusion 360 add-in
Follow `bridge/OttoEngineSysMLBridge/README.md`, then edit `bridge/OttoEngineSysMLBridge/config.json` for your API host and part name.

## Project status
- SysML model: complete and annotated with Fusion metadata placeholders.
- API tooling: working client for listing projects, extracting parameters, and generating Fusion scripts.
- Fusion integration: add-in skeleton with sync commands; commit or upload behavior depends on the SysML API version.

## More docs
- `docs/project/otto_engine_project_review.md`: project review and outputs.
- `docs/api/`: upload guidance and troubleshooting notes.
- `docs/model/`: state diagrams and requirements table.
