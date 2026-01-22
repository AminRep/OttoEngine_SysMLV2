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

## OttoEngine MVP simulation
This MVP pulls key inputs from SysON and runs a lightweight deterministic analysis in Python.

### Prerequisites
- Python 3.9+
- `requests` (optional; SysMLv2Client falls back to urllib)
- `pytest` (only if running tests)

### Run
```bash
python tools/run_otto_mvp.py --host http://localhost:8081/api/rest --project OttoEngine --part fourCylinderEngine --out outputs/otto_mvp --rpm 3000
```

### Outputs
- `outputs/otto_mvp/inputs_raw.json`: raw parameters from SysON (or offline input)
- `outputs/otto_mvp/inputs_resolved.json`: canonical inputs used for simulation
- `outputs/otto_mvp/diagnostics.json`: mapping details, assumptions, and overrides
- `outputs/otto_mvp/results.json`: computed metrics (displacement, mean piston speed, efficiency, optional power)
- `outputs/otto_mvp/report.md`: human-readable summary

### Offline mode
If SysON is unavailable, use the fixture:
```bash
python tools/run_otto_mvp.py --offline tools/fixtures/ottoengine_raw_params.json --out outputs/otto_mvp
```

### MATLAB extension (later)
The MVP outputs stable JSON artifacts (`inputs_resolved.json` and `results.json`). A future MATLAB
integration can read the same canonical inputs (bore_m, stroke_m, compression_ratio, n_cylinders,
rpm) and append MATLAB-specific results without changing the CLI contract.

## Project status
- SysML model: complete and annotated with Fusion metadata placeholders.
- API tooling: working client for listing projects, extracting parameters, and generating Fusion scripts.
- Fusion integration: add-in skeleton with sync commands; commit or upload behavior depends on the SysML API version.

## More docs
- `docs/project/otto_engine_project_review.md`: project review and outputs.
- `docs/api/`: upload guidance and troubleshooting notes.
- `docs/model/`: state diagrams and requirements table.
