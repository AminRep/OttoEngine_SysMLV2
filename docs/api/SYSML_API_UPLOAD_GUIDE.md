# How to Upload .sysml Files to the SysML v2 API

Your SysML v2 API is running on `http://localhost:9000`. Here's how to publish your `.sysml` files to it.

## Quick Overview

The SysML v2 API works with:
- **Projects**: Containers for your models
- **Commits**: Versions of your model content
- **Elements**: The actual SysML model elements (parts, packages, etc.)

## Method 1: Using Python Script (Recommended)

### Step 1: Install requirements
```bash
pip install requests
```

### Step 2: Run the upload script
```bash
python quick_upload_example.py
```

Or upload a specific file:
```bash
python upload_sysml_to_api.py ottoZyklus.sysml "My Engine Project"
```

## Method 2: Using curl (Command Line)

### Step 1: Test API connection
```bash
curl http://localhost:9000/projects
```

Expected response: List of existing projects (might be empty: `[]`)

### Step 2: Create a new project
```bash
curl -X POST http://localhost:9000/projects \
  -H "Content-Type: application/json" \
  -d "{\"@type\": \"Project\", \"name\": \"Ottomotor Project\", \"description\": \"My engine model\"}"
```

Expected response: JSON with project details including `@id` field.
**Save the project ID!** You'll need it for the next step.

### Step 3: Upload your SysML file
```bash
curl -X POST http://localhost:9000/projects/{PROJECT_ID}/commits \
  -H "Content-Type: text/plain; charset=utf-8" \
  --data-binary @ottoZyklus.sysml
```

Replace `{PROJECT_ID}` with the ID from Step 2.

Example:
```bash
curl -X POST http://localhost:9000/projects/01234567-89ab-cdef-0123-456789abcdef/commits \
  -H "Content-Type: text/plain; charset=utf-8" \
  --data-binary @ottoZyklus.sysml
```

### Step 4: Verify the upload
```bash
curl http://localhost:9000/projects/{PROJECT_ID}/commits
```

This shows all commits in your project.

To see the elements:
```bash
curl http://localhost:9000/projects/{PROJECT_ID}/commits/{COMMIT_ID}/elements
```

## Method 3: Using Python requests library directly

```python
import requests

API_URL = "http://localhost:9000"

# 1. Create a project
project_data = {
    "@type": "Project",
    "name": "Ottomotor Project"
}
response = requests.post(f"{API_URL}/projects", json=project_data)
project = response.json()
project_id = project['@id']

# 2. Read your SysML file
with open('ottoZyklus.sysml', 'r', encoding='utf-8') as f:
    sysml_content = f.read()

# 3. Upload it
response = requests.post(
    f"{API_URL}/projects/{project_id}/commits",
    headers={"Content-Type": "text/plain; charset=utf-8"},
    data=sysml_content
)

commit = response.json()
print(f"Uploaded! Commit ID: {commit['@id']}")

# 4. Get elements
elements = requests.get(
    f"{API_URL}/projects/{project_id}/commits/{commit['@id']}/elements"
).json()

print(f"Found {len(elements)} elements!")
```

## Common API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/projects` | GET | List all projects |
| `/projects` | POST | Create a new project |
| `/projects/{id}` | GET | Get project details |
| `/projects/{id}/commits` | GET | List commits in project |
| `/projects/{id}/commits` | POST | Upload SysML content (creates commit) |
| `/projects/{id}/commits/{commitId}/elements` | GET | Get all elements |
| `/projects/{id}/commits/{commitId}/elements/{elementId}` | GET | Get specific element |

## Troubleshooting

### "Cannot connect to API"
- Make sure the API server is running: `docker-compose up`
- Check if port 9000 is accessible: `curl http://localhost:9000/projects`
- Check Docker containers: `docker ps`

### "Upload fails with 400/500 error"
- Check your SysML syntax is valid
- Make sure the file is UTF-8 encoded
- Try uploading a simpler SysML file first to test

### "No elements found after upload"
- The API might still be parsing your file
- Check the commit was created successfully
- Look at API server logs for parsing errors

## Files You Can Upload

You have these SysML files available:
- `ottoZyklus.sysml` - Your Otto cycle engine model
- `ottomotor_with_fusion_placeholders.sysml` - Engine with Fusion 360 metadata
- `archive/EV_BTMS.sysml` - Battery thermal management system
- `archive/learningSyntax.sysml` - Syntax examples
- `archive/stateMachine.sysml` - State machine example

## Next Steps After Upload

1. **Query your model**: Use GET requests to retrieve elements
2. **Update elements**: Use PUT requests to modify elements
3. **Connect to Fusion 360**: Use the metadata in your model to link to Fusion files
4. **Create branches**: The API supports branching for version control

## Example Workflow

```bash
# 1. Check what's on the server
curl http://localhost:9000/projects

# 2. Create a project
curl -X POST http://localhost:9000/projects \
  -H "Content-Type: application/json" \
  -d '{"@type": "Project", "name": "Test Project"}'

# 3. Upload your file (replace PROJECT_ID)
curl -X POST http://localhost:9000/projects/PROJECT_ID/commits \
  -H "Content-Type: text/plain" \
  --data-binary @ottoZyklus.sysml

# 4. See what was created
curl http://localhost:9000/projects/PROJECT_ID/commits/COMMIT_ID/elements
```

## Using with Your Existing Code

You can integrate this into your `api_learning_playground.py`:

```python
# Add to the RealSysMLv2API class:

def upload_sysml_file(self, project_id: str, file_path: str) -> bool:
    """Upload a .sysml file to a project"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    response = requests.post(
        f"{self.host}/projects/{project_id}/commits",
        headers={"Content-Type": "text/plain; charset=utf-8"},
        data=content
    )

    return response.status_code in [200, 201]
```

---

**Ready to try?** Run:
```bash
python quick_upload_example.py
```
