"""
Simple script to upload/update ottoengine.sysml to SysON OttoEngine project
"""

import requests
import json

# Configuration
SYSON_BASE_URL = "http://localhost:8080"  # Change if your SysON is hosted elsewhere
PROJECT_NAME = "OttoEngine"
SYSML_FILE_PATH = "ottoengine.sysml"


def find_project_id(base_url: str, project_name: str) -> str:
    """Find the project ID by name"""
    url = f"{base_url}/api/rest/projects"
    response = requests.get(url)
    response.raise_for_status()

    projects = response.json()
    for project in projects.get('items', []):
        if project.get('name') == project_name:
            return project.get('@id')

    raise Exception(f"Project '{project_name}' not found!")


def upload_via_graphql(base_url: str, project_id: str, file_path: str):
    """
    Alternative method: Upload using GraphQL mutation
    SysON uses GraphQL for some operations
    """
    url = f"{base_url}/api/graphql"

    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # GraphQL mutation for uploading document
    mutation = """
    mutation uploadDocument($input: UploadDocumentInput!) {
        uploadDocument(input: $input) {
            __typename
            ... on UploadDocumentSuccessPayload {
                document {
                    id
                    name
                }
            }
            ... on ErrorPayload {
                message
            }
        }
    }
    """

    variables = {
        "input": {
            "id": str(uuid.uuid4()),
            "editingContextId": project_id,
            "file": file_content,
            "checkProxyResolution": False
        }
    }

    response = requests.post(url, json={
        "query": mutation,
        "variables": variables
    })

    return response.json()


def check_available_endpoints(base_url: str):
    """Fetch OpenAPI spec to see available endpoints"""
    api_docs_url = f"{base_url}/v3/api-docs/rest-apis"

    try:
        response = requests.get(api_docs_url)
        response.raise_for_status()
        api_spec = response.json()

        print("\nAvailable REST API Endpoints:")
        print("=" * 60)
        for path, methods in api_spec.get('paths', {}).items():
            for method, details in methods.items():
                summary = details.get('summary', 'No description')
                print(f"{method.upper():<8} {path}")
                print(f"         └─ {summary}")
        print("=" * 60)

        return api_spec

    except Exception as e:
        print(f"Could not fetch API documentation: {e}")
        print(f"\nPlease visit Swagger UI manually at:")
        print(f"{base_url}/swagger-ui/index.html")
        return None


def main():
    print("=" * 70)
    print("SysON OttoEngine Uploader")
    print("=" * 70)

    # Step 1: Find the project
    print(f"\n[Step 1] Finding '{PROJECT_NAME}' project...")
    try:
        project_id = find_project_id(SYSON_BASE_URL, PROJECT_NAME)
        print(f"✓ Found project with ID: {project_id}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    # Step 2: Check available API endpoints
    print(f"\n[Step 2] Checking available API endpoints...")
    api_spec = check_available_endpoints(SYSON_BASE_URL)

    # Step 3: Upload instructions
    print("\n[Step 3] Uploading the file...")
    print("\n⚠ IMPORTANT:")
    print("The SysON REST API documentation doesn't expose a direct file upload endpoint.")
    print("\nYou have two options:\n")

    print("OPTION A - Use the SysON Web UI (Recommended):")
    print("  1. Open your browser and go to your SysON instance")
    print("  2. Navigate to the OttoEngine project")
    print("  3. Open the Project Explorer view")
    print("  4. Click the 'Upload' button")
    print(f"  5. Select '{SYSML_FILE_PATH}'")
    print("  6. Choose 'read-write' mode")
    print("  7. Confirm the upload")

    print("\nOPTION B - Check Swagger UI for undocumented endpoints:")
    print(f"  1. Visit: {SYSON_BASE_URL}/swagger-ui/index.html")
    print("  2. Look for endpoints containing 'upload', 'document', or 'file'")
    print("  3. Test the endpoint with your ottoengine.sysml file")
    print("  4. Update this script with the working endpoint")

    print("\nOPTION C - Use GraphQL API (Advanced):")
    print("  SysON also has a GraphQL API at /api/graphql")
    print("  This might have upload mutations not in the REST API")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    import uuid  # for GraphQL option
    main()
