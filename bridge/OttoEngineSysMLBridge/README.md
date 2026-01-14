# OttoEngineSysMLBridge - Fusion 360 Add-In

Bidirectional parameter synchronization between SysML v2 models and Fusion 360.

Based on: *"Praktische Anwendung der SysML v2 API am Beispiel von MCAD und Simulation"* (Manoury & Muggeo, TdSE 2023)

## Features

- **Sync From SysML**: Pull parameters from SysML v2 model and update Fusion 360 user parameters
- **Sync To SysML**: Push Fusion 360 parameters back to SysML v2 model
- **Configurable Mappings**: Define parameter mappings in `lib/parameter_mapper.py`
- **Bidirectional Sync**: Support for `toFusion`, `fromFusion`, and `both` directions

## Installation

### 1. Install the Add-In

1. Copy the entire `OttoEngineSysMLBridge` folder to your Fusion 360 add-ins directory:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **Mac**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

2. Open Fusion 360

3. Go to **Tools > Add-Ins > Scripts and Add-Ins**

4. In the **Add-Ins** tab, find **OttoEngineSysMLBridge**

5. Click **Run** to start the add-in

### 2. Configure the Add-In

Edit `config.json` to match your setup:

```json
{
    "sysml_api": {
        "host": "http://localhost:8081/api/rest",
        "project_name": "OttoEngine",
        "default_part": "fourCylinderEngine"
    },
    "sync_settings": {
        "auto_sync_on_change": false,
        "sync_direction": "toFusion",
        "confirm_before_sync": true
    }
}
```

## Usage

### Sync From SysML (Pull Parameters)

1. Make sure your SysML v2 API server is running on `localhost:8081`

2. In Fusion 360, look for the **SysML Bridge** panel in your toolbar

3. Click **Sync From SysML**

4. Enter the SysML part name (default: `fourCylinderEngine`)

5. Click **OK**

6. The add-in will:
   - Connect to the SysML v2 API
   - Extract parameters from your SysML model
   - Create/update Fusion 360 user parameters
   - Show a summary of updated parameters

### Sync To SysML (Push Parameters)

1. Click **Sync To SysML** in the SysML Bridge panel

2. Enter the SysML part name

3. Click **OK**

4. Review the parameters that will be synced

**Note**: The actual SysML commit implementation depends on your specific SysML v2 API version and model structure.

## Project Structure

```
OttoEngineSysMLBridge/
├── OttoEngineSysMLBridge.py      # Main add-in entry point
├── OttoEngineSysMLBridge.manifest # Add-in metadata
├── config.json                    # Configuration file
├── README.md                      # This file
├── commands/
│   ├── __init__.py
│   ├── sync_from_sysml.py        # Pull parameters from SysML
│   └── sync_to_sysml.py          # Push parameters to SysML
└── lib/
    ├── __init__.py
    ├── sysml_api.py              # SysML v2 API client
    └── parameter_mapper.py       # Parameter mapping logic
```

## Parameter Mapping

Parameters are mapped in `lib/parameter_mapper.py`:

```python
PARAMETER_MAP = {
    "bore": ("bore_diameter", "toFusion", "dimension", "mm"),
    "stroke": ("stroke_length", "toFusion", "dimension", "mm"),
    "mass": ("total_mass", "both", "mass", "kg"),
    # ... more mappings
}
```

Format: `sysml_attr -> (fusion_param_name, sync_direction, param_type, unit)`

### Sync Directions

- **`toFusion`**: Only sync from SysML to Fusion 360
- **`fromFusion`**: Only sync from Fusion 360 to SysML
- **`both`**: Bidirectional sync

## Requirements

- Fusion 360
- SysML v2 API server running (typically on `localhost:8081`)
- Python `requests` library (optional, uses `urllib` as fallback)
- OttoEngine SysML v2 project

## Troubleshooting

### Add-in doesn't appear

- Make sure you copied the **entire folder** to the AddIns directory
- Restart Fusion 360
- Check the add-in is enabled in Tools > Add-Ins

### Cannot connect to SysML API

- Verify the SysML v2 API server is running
- Check the `host` in `config.json` matches your server URL
- Test connection with: `python sysml_fusion_bridge.py --test-connection`

### No parameters found

- Verify the part name matches exactly (case-sensitive)
- Check that your SysML model has the expected part
- Use the standalone script to debug: `python sysml_fusion_bridge.py --extract <partName>`

## Development

To modify parameter mappings or add new features:

1. Edit the appropriate module in `lib/` or `commands/`
2. Restart the add-in in Fusion 360 (Stop > Run)
3. Test your changes

## License

Based on the research paper and example code from TdSE 2023.

## Support

For issues and questions, refer to the original research paper or consult your SysML v2 API documentation.
