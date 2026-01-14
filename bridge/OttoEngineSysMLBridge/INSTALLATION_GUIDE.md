# OttoEngine SysML Bridge - Installation Guide

## What Was Fixed

Your add-in had several structural issues that prevented it from loading in Fusion 360:

1. **Wrong Location**: Add-ins were in `AddIns` folder instead of `ApplicationPlugins`
2. **Wrong Structure**: Missing `.bundle` structure with `PackageContents.xml`
3. **Type Hints**: Python type hints caused compatibility issues with Fusion 360
4. **Module Organization**: Import structure didn't match Fusion's expectations

## New Structure

The add-in is now properly structured as:

```
ApplicationPlugins/
└── OttoEngineSysMLBridge.bundle/
    ├── PackageContents.xml          # Registers plugin with Fusion
    └── Contents/
        ├── OttoEngineSysMLBridge.py # Main entry point
        ├── OttoEngineSysMLBridge.manifest
        ├── config.py                 # Debug settings
        ├── config.json              # SysML API configuration
        ├── commands/                # Command modules
        │   ├── __init__.py
        │   ├── syncFromSysML.py
        │   └── syncToSysML.py
        ├── lib/                     # Library modules
        │   ├── fusionAddInUtils/    # Fusion utilities
        │   ├── sysml_api.py         # SysML API client
        │   └── parameter_mapper.py  # Parameter mapping
        └── resources/               # Icons (optional)
```

## Installation Steps

### The add-in is ALREADY INSTALLED in:
```
C:\Users\Asus\AppData\Roaming\Autodesk\ApplicationPlugins\OttoEngineSysMLBridge.bundle
```

### To Test:

1. **Close Fusion 360** if it's running

2. **Restart Fusion 360**

3. **Check if the add-in loaded**:
   - The add-in should load automatically on startup
   - Look for the "SysML Bridge" panel in your toolbar
   - You should see two buttons: "Sync From SysML" and "Sync To SysML"

4. **If you don't see it**:
   - Go to **Tools > Add-Ins** (Shift+S)
   - Look under "Add-Ins" tab
   - Find "OttoEngine SysML Bridge"
   - Click "Run" to manually start it

## Testing the Add-In

### Test 1: Check if it loads

1. Open Fusion 360
2. Look for "SysML Bridge" panel in toolbar
3. If you see it with two buttons → SUCCESS!

### Test 2: Try Sync From SysML

1. Ensure your SysML v2 API server is running on http://localhost:8081
2. Open or create a design in Fusion 360
3. Click "Sync From SysML" button
4. Enter the part name (default: fourCylinderEngine)
5. Click OK

**Expected Results**:
- If SysML server is running and has the project: Parameters will be synced
- If SysML server is not running: Error message about connection
- Either way, the command should execute without crashing

### Test 3: Try Sync To SysML

1. Ensure you have user parameters in your Fusion design
2. Click "Sync To SysML" button
3. Enter the part name
4. Click OK

**Expected Results**:
- Shows a preview of what would be synced
- (Full sync to SysML requires additional implementation)

## Troubleshooting

### Add-in doesn't appear

1. Check that the folder exists:
   ```
   C:\Users\Asus\AppData\Roaming\Autodesk\ApplicationPlugins\OttoEngineSysMLBridge.bundle
   ```

2. Check the Text Commands window in Fusion (View > Text Commands) for error messages

3. Try manually running from Scripts and Add-Ins:
   - Press Shift+S
   - Go to Add-Ins tab
   - Look for "OttoEngine SysML Bridge"
   - Click "Run"

### Error messages

- **"Cannot connect to SysML API"**: Start your SysML v2 API server
- **"Project not found"**: Check project name in config.json
- **"No active design"**: Open or create a design before syncing

## Configuration

Edit this file to change settings:
```
C:\Users\Asus\AppData\Roaming\Autodesk\ApplicationPlugins\OttoEngineSysMLBridge.bundle\Contents\config.json
```

Default settings:
```json
{
    "sysml_api": {
        "host": "http://localhost:8081/api/rest",
        "project_name": "OttoEngine",
        "default_part": "fourCylinderEngine"
    }
}
```

## Success Criteria

✅ Fusion 360 starts without errors
✅ "SysML Bridge" panel appears in toolbar
✅ Two buttons are visible: "Sync From SysML" and "Sync To SysML"
✅ Clicking buttons opens dialog (doesn't crash)
✅ Commands execute and show results or error messages

## Next Steps

Once the add-in is working:

1. Configure your SysML API connection in config.json
2. Ensure your SysML model has the correct parameter names
3. Test syncing parameters back and forth
4. If you need to add custom icons, place PNG files in the `resources/` folder

## Comparison with Old Structure

**OLD (Broken)**:
```
AddIns/OttoEngineSysMLBridge/
├── OttoEngineSysMLBridge.py
├── OttoEngineSysMLBridge.manifest
├── commands/
└── lib/
```

**NEW (Working)**:
```
ApplicationPlugins/OttoEngineSysMLBridge.bundle/
├── PackageContents.xml
└── Contents/
    ├── OttoEngineSysMLBridge.py
    ├── OttoEngineSysMLBridge.manifest
    ├── commands/
    └── lib/
```

The key differences are:
1. `.bundle` extension on folder
2. `PackageContents.xml` at root
3. Everything inside `Contents/` subfolder
4. Located in `ApplicationPlugins` not `AddIns`
