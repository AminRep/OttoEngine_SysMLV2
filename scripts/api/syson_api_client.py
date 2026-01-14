"""
SysON REST API Client for Managing SysML Projects
This script helps you interact with SysON to upload and manage .sysml files
"""

import requests
import json
from typing import Optional, Dict, Any

class SysONClient:
    """Client for interacting with SysON REST API"""

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize the SysON API client

        Args:
            base_url: Base URL of your SysON server (default: http://localhost:8080)
        """
        self.base_url = base_url
        self.api_base = f"{base_url}/api/rest"
        self.session = requests.Session()

    def get_projects(self) -> Dict[str, Any]:
        """Get all projects in SysON"""
        url = f"{self.api_base}/projects"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def find_project_by_name(self, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Find a project by name

        Args:
            project_name: Name of the project to find (e.g., "OttoEngine")

        Returns:
            Project data if found, None otherwise
        """
        projects = self.get_projects()
        for project in projects.get('items', []):
            if project.get('name') == project_name:
                return project
        return None

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get a specific project by ID"""
        url = f"{self.api_base}/projects/{project_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def create_project(self, name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new project

        Args:
            name: Project name
            description: Optional project description

        Returns:
            Created project data
        """
        url = f"{self.api_base}/projects"
        params = {"name": name}
        if description:
            params["description"] = description

        response = self.session.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_commits(self, project_id: str) -> Dict[str, Any]:
        """Get commits for a project (SysON typically has one commit per project)"""
        url = f"{self.api_base}/projects/{project_id}/commits"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_elements(self, project_id: str, commit_id: str) -> Dict[str, Any]:
        """Get all elements in a project/commit"""
        url = f"{self.api_base}/projects/{project_id}/commits/{commit_id}/elements"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def upload_sysml_file(self, project_id: str, file_path: str) -> Dict[str, Any]:
        """
        Upload a .sysml file to a project

        NOTE: This endpoint may vary depending on SysON version.
        Check Swagger UI at http://localhost:8080/swagger-ui/ for the exact endpoint.

        Args:
            project_id: UUID of the target project
            file_path: Path to the .sysml file

        Returns:
            API response
        """
        # Try common upload endpoint patterns
        possible_endpoints = [
            f"{self.base_url}/api/projects/{project_id}/upload",
            f"{self.base_url}/api/rest/projects/{project_id}/upload",
            f"{self.base_url}/api/rest/projects/{project_id}/documents",
        ]

        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('\\')[-1], f, 'text/plain')}

            for endpoint in possible_endpoints:
                try:
                    response = self.session.post(endpoint, files=files)
                    if response.status_code == 200:
                        return response.json()
                except Exception as e:
                    continue

        raise Exception(
            "Upload endpoint not found. Please check Swagger UI at "
            f"{self.base_url}/swagger-ui/ for the correct upload endpoint"
        )

    def check_swagger_docs(self):
        """Print the Swagger UI URL for API documentation"""
        swagger_url = f"{self.base_url}/swagger-ui/index.html"
        api_docs_url = f"{self.base_url}/v3/api-docs/rest-apis"
        print(f"Swagger UI: {swagger_url}")
        print(f"API Docs JSON: {api_docs_url}")
        return swagger_url


def main():
    """Example usage of the SysON API client"""

    # Initialize client
    client = SysONClient(base_url="http://localhost:8080")

    print("=" * 60)
    print("SysON API Client - OttoEngine Project Manager")
    print("=" * 60)

    # 1. List all projects
    print("\n1. Fetching all projects...")
    try:
        projects = client.get_projects()
        print(f"Found {len(projects.get('items', []))} projects:")
        for project in projects.get('items', []):
            print(f"  - {project.get('name')} (ID: {project.get('@id')})")
    except Exception as e:
        print(f"Error fetching projects: {e}")

    # 2. Find OttoEngine project
    print("\n2. Looking for 'OttoEngine' project...")
    try:
        otto_project = client.find_project_by_name("OttoEngine")
        if otto_project:
            project_id = otto_project.get('@id')
            print(f"Found OttoEngine project!")
            print(f"  Project ID: {project_id}")
            print(f"  Name: {otto_project.get('name')}")

            # 3. Get commits (SysON uses single commit)
            print("\n3. Fetching commits...")
            commits = client.get_commits(project_id)
            commit_id = commits.get('items', [{}])[0].get('@id', project_id)
            print(f"  Commit ID: {commit_id}")

            # 4. Attempt to upload the file
            print("\n4. Uploading ottoengine.sysml...")
            print("NOTE: Direct file upload endpoint may not be available.")
            print("Check Swagger UI for available endpoints:")
            client.check_swagger_docs()

        else:
            print("OttoEngine project not found.")
            print("Would you like to create it? (This requires manual confirmation)")

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Check Swagger UI at http://localhost:8080/swagger-ui/")
    print("2. Look for upload/document endpoints")
    print("3. Update this script with the correct endpoint")
    print("4. Or use the SysON UI Upload feature for now")


if __name__ == "__main__":
    main()
