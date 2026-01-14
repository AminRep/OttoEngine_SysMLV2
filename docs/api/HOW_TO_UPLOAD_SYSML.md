# How to Upload .sysml Files to Your SysML v2 API

## Summary

Your SysML v2 API is running on `http://localhost:9000`. Here's what I discovered:

### What Works
- API is accessible and running
- Creating projects works: `POST /projects`
- Getting projects works: `GET /projects`

### The Challenge
The SysML v2 API expects a **specific format** for uploading model content. Based on the error we encountered, uploading raw `.sysml` text files directly to `/commits` endpoint is not the correct approach.

## Recommended Solutions

### Solution 1: Use the SysML v2 API Cookbook (Best)

The official repository mentioned in your API's README provides examples:
https://github.com/Systems-Modeling/SysML-v2-API-Cookbook

This cookbook contains working examples of how to properly upload SysML models to the API.

### Solution 2: Use the Swagger Documentation

Your API has built-in documentation at:
```
http://localhost:9000/docs/
```

Open this in your web browser to see:
- All available API endpoints
- Required data formats
- Example requests and responses
- Interactive API testing

### Solution 3: What We Successfully Tested

```python
import requests

API_URL = "http://localhost:9000"

# This works - Creating a project
project_data = {
    "@type": "Project",
    "name": "My Ottomotor Project",
    "description": "Engine model"
}

response = requests.post(
    f"{API_URL}/projects",
    headers={"Content-Type": "application/json"},
    json=project_data
)

project = response.json()
print(f"Project ID: {project['@id']}")

# Check the project was created
response = requests.get(f"{API_URL}/projects/{project['@id']}")
print(response.json())
```

**This successfully created project:** `3dce91c7-965c-4aed-a36e-bb82875fe559`

## Next Steps

### Option A: Use Postman (Visual/Interactive)

1. Check if there's a Postman collection in your API folder:
   ```bash
   cat SysML-v2-API-Services/postman.json
   ```

2. Import this into Postman to see working examples

3. Postman provides a visual interface to test the API

### Option B: Check the API Cookbook

```bash
# Clone the cookbook
git clone https://github.com/Systems-Modeling/SysML-v2-API-Cookbook

# Look for Python examples
cd SysML-v2-API-Cookbook
ls -la
```

### Option C: Check Swagger Documentation

1. Open browser to: `http://localhost:9000/docs/`

2. Look for the `/commits` endpoint

3. Check the expected request body format

4. Test directly in Swagger UI

## Understanding the API Structure

Based on what works, the API follows this structure:

```
Projects (Container for your models)
  └─ Branches (like git branches)
      └─ Commits (versions of your model)
          └─ Elements (actual SysML parts/definitions)
```

### Working Example Flow

```bash
# 1. Create a project
curl -X POST http://localhost:9000/projects \
  -H "Content-Type: application/json" \
  -d '{"@type": "Project", "name": "Test"}'

# Response includes: @id (project ID) and defaultBranch.@id (branch ID)

# 2. Get the default branch
curl http://localhost:9000/projects/{PROJECT_ID}

# 3. Upload content to the branch/commit
# (Format to be determined from Swagger docs or Cookbook)
```

## Files Included in This Package

1. **quick_upload_example.py** - Working script that creates projects
2. **upload_sysml_to_api.py** - More complete uploader (needs format fix)
3. **SYSML_API_UPLOAD_GUIDE.md** - General guide
4. **HOW_TO_UPLOAD_SYSML.md** (this file) - What we learned

## Your Available SysML Files

Ready to upload once we have the correct format:
- [ottoZyklus.sysml](ottoZyklus.sysml) - 16,845 characters
- [ottomotor_with_fusion_placeholders.sysml](ottomotor_with_fusion_placeholders.sysml)
- [archive/EV_BTMS.sysml](archive/EV_BTMS.sysml)
- [archive/learningSyntax.sysml](archive/learningSyntax.sysml)
- [archive/stateMachine.sysml](archive/stateMachine.sysml)

## Quick Commands Reference

```bash
# Check API is running
curl http://localhost:9000/projects

# View Swagger docs
# Open in browser: http://localhost:9000/docs/

# Create a project (confirmed working)
curl -X POST http://localhost:9000/projects \
  -H "Content-Type: application/json" \
  -d '{"@type": "Project", "name": "Ottomotor", "description": "Engine model"}'

# List all projects
curl http://localhost:9000/projects

# Get specific project (replace ID)
curl http://localhost:9000/projects/3dce91c7-965c-4aed-a36e-bb82875fe559

# View Postman collection
cat SysML-v2-API-Services/postman.json
```

## Troubleshooting

### If the Commit Upload Fails (500 error)
This means the API expects a different format than raw text. Solutions:
1. Check the Swagger docs for the exact format
2. Check the Postman collection for working examples
3. Review the API Cookbook repository

### If You Get Connection Errors
```bash
# Check if API is running
curl http://localhost:9000/projects

# Restart API if needed
cd SysML-v2-API-Services
sbt run
```

### If You Need to See API Logs
```bash
# Check the logs directory
tail -f SysML-v2-API-Services/logs/application.log
```

## What's Next?

1. **Immediate**: Open `http://localhost:9000/docs/` in your browser
2. **Look for**: The correct format for the `/commits` endpoint
3. **Test**: Use Swagger UI to test uploading
4. **Reference**: Check the Postman collection or API Cookbook

Once you find the correct format from the docs, I can update the Python scripts to match!
