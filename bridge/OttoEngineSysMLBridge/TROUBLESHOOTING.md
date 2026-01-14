# OttoEngineSysMLBridge - Troubleshooting Guide

## Issues Found and Fixed

### Problem 1: Type Hints Not Compatible with Fusion 360
**Issue:** Python type hints (`from typing import Dict, List, Optional, Any`) can cause import failures in Fusion 360's Python environment.

**Solution:** Removed all type hint imports and annotations from:
- `lib/sysml_api.py`
- `lib/parameter_mapper.py`

### Problem 2: Early Module Imports
**Issue:** The original code imported command modules at startup, which could fail if any dependencies were missing.

**Solution:** Changed to lazy imports - modules are only imported when the user clicks a button.

### Problem 3: Missing Resources Folder
**Issue:** Code referenced `'./resources'` for icons, but folder doesn't exist.

**Solution:** Removed the resources parameter from button definitions (icons are optional).

## How to Test

### Step 1: Run Diagnostic Version
1. In Fusion 360, open Scripts and Add-Ins (Shift+S)
2. Select the "Add-Ins" tab
3. Click the "+" button next to "My Add-Ins"
4. Navigate to: `C:\Users\Asus\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns\OttoEngineSysMLBridge`
5. Select `OttoEngineSysMLBridge_diagnostic.py`
6. Click "Run"
7. Follow the message boxes to see where the import fails

### Step 2: Use Fixed Version
1. Rename the original file:
   - `OttoEngineSysMLBridge.py` → `OttoEngineSysMLBridge_original.py`
2. Rename the fixed file:
   - `OttoEngineSysMLBridge_fixed.py` → `OttoEngineSysMLBridge.py`
3. Restart Fusion 360
4. The add-in should now load automatically (if runOnStartup is true) or appear in Scripts and Add-Ins

### Step 3: Verify It Works
1. Look for the "SysML Bridge" panel in your toolbar
2. You should see two buttons: "Sync From SysML" and "Sync To SysML"
3. Click one to test (it will show an error if the SysML API server isn't running, but that's expected)

## Common Errors

### "No active design found"
- Open or create a design in Fusion 360 before running sync commands

### "Project 'OttoEngine' not found"
- Ensure the SysML v2 API server is running on localhost:8081
- Check that the project name in `config.json` matches your SysML project

### "Cannot connect to http://localhost:8081"
- Start the SysML v2 API server
- Verify the host URL in `config.json` is correct

## Files Modified

1. **OttoEngineSysMLBridge.py** (main file)
   - Removed early imports
   - Changed to lazy imports
   - Removed resources path
   - Better error handling

2. **lib/sysml_api.py**
   - Removed all type hints
   - Removed typing module import

3. **lib/parameter_mapper.py**
   - Removed all type hints
   - Removed typing module import

## Next Steps

If the add-in still doesn't work:
1. Run the diagnostic version to identify the exact import that's failing
2. Check Fusion 360's Python version (Help > About Fusion 360 > Show Details)
3. Check the Text Commands window in Fusion for any error messages
