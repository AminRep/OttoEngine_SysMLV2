#!/usr/bin/env python3
"""
sysml_fusion_bridge.py - SysML v2 to Fusion 360 Bridge

Based on: "Praktische Anwendung der SysML v2 API am Beispiel von MCAD und Simulation"
          (Manoury & Muggeo, TdSE 2023)

This script can be run:
1. Standalone to test SysML v2 API communication
2. Imported by Fusion 360 add-ins

Usage:
    python sysml_fusion_bridge.py --list-projects
    python sysml_fusion_bridge.py --extract fourCylinderEngine
    python sysml_fusion_bridge.py --test-connection
    python sysml_fusion_bridge.py --extract fourCylinderEngine --generate-fusion-script
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Any

try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    USE_REQUESTS = False


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_HOST = "http://localhost:8081/api/rest"

# Parameter mapping based on @FusionParameter metadata in OttoEngine.sysml (English version)
# Format: sysml_attr -> (fusion_param_name, sync_direction, param_type, unit)
PARAMETER_MAP = {
    # Piston
    "diameter": ("piston_diameter", "toFusion", "dimension", "mm"),
    "height": ("piston_height", "toFusion", "dimension", "mm"),
    "pinDiameter": ("pin_diameter", "toFusion", "dimension", "mm"),
    
    # Cylinder
    "bore": ("bore_diameter", "toFusion", "dimension", "mm"),
    "stroke": ("stroke_length", "toFusion", "dimension", "mm"),
    "displacement": ("displacement", "fromFusion", "dimension", "L"),
    "compressionRatio": ("compression_ratio", "toFusion", "dimension", ""),
    
    # ConnectingRod
    "length": ("conrod_length", "toFusion", "dimension", "mm"),
    "smallEndDiameter": ("small_end_dia", "toFusion", "dimension", "mm"),
    "bigEndDiameter": ("big_end_dia", "toFusion", "dimension", "mm"),
    
    # Crankshaft
    "crankRadius": ("crank_radius", "toFusion", "dimension", "mm"),
    
    # OttoEngine (assembly level)
    "mass": ("total_mass", "both", "mass", "kg"),
    "totalDisplacement": ("total_displacement", "toFusion", "dimension", "L"),
    "ratedPower": ("rated_power", "toFusion", "dimension", "kW"),
    "maxTorque": ("max_torque", "toFusion", "dimension", "N*m"),
    "numberOfCylinders": ("cylinder_count", "toFusion", "dimension", ""),
    
    # Valve attributes
    "headDiameter": ("valve_head_dia", "toFusion", "dimension", "mm"),
    "stemDiameter": ("valve_stem_dia", "toFusion", "dimension", "mm"),
    "lift": ("valve_lift", "toFusion", "dimension", "mm"),
    
    # SparkPlug attributes
    "threadSize": ("spark_thread_size", "toFusion", "dimension", "mm"),
    "electrodeGap": ("spark_electrode_gap", "toFusion", "dimension", "mm"),
    "heatRange": ("spark_heat_range", "toFusion", "dimension", ""),
}


# ============================================================================
# SysML v2 API CLIENT
# ============================================================================

class SysMLv2Client:
    """
    Client for SysML v2 REST API
    
    Implements conformance tests from the paper:
    - PIM-PS-002 (Get Projects)
    - PIM-EN-001 (Get Elements)  
    - PIM-PCB-010 (Create Commit)
    """
    
    def __init__(self, host: str = DEFAULT_HOST):
        self.host = host.rstrip('/')
        self.project_id: Optional[str] = None
        self.commit_id: Optional[str] = None
        self._cache: Dict[str, Any] = {}
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[dict] = None) -> Optional[Any]:
        """Make HTTP request to API"""
        url = f"{self.host}{endpoint}"
        
        if USE_REQUESTS:
            try:
                if method == "GET":
                    resp = requests.get(url, timeout=10)
                elif method == "POST":
                    resp = requests.post(
                        url, 
                        json=data,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                else:
                    return None
                
                if resp.ok:
                    return resp.json()
                else:
                    print(f"API Error: {resp.status_code} - {resp.text[:200]}")
                    return None
            except requests.exceptions.ConnectionError:
                print(f"[ERROR] Cannot connect to {self.host}")
                print("   Is the SysML v2 API server running?")
                return None
            except Exception as e:
                print(f"[ERROR] Request failed: {e}")
                return None
        else:
            # urllib fallback
            try:
                req = urllib.request.Request(url)
                req.add_header("Content-Type", "application/json")
                
                body = json.dumps(data).encode('utf-8') if data else None
                
                with urllib.request.urlopen(req, data=body, timeout=10) as response:
                    return json.loads(response.read().decode('utf-8'))
            except urllib.error.URLError as e:
                print(f"[ERROR] Cannot connect: {e}")
                return None
            except Exception as e:
                print(f"[ERROR] Request failed: {e}")
                return None
    
    # -------------------------------------------------------------------------
    # Project Operations (PIM-PS-002, PIM-PS-003)
    # -------------------------------------------------------------------------
    
    def get_projects(self) -> List[dict]:
        """PIM-PS-002: List all projects in repository"""
        result = self._request("GET", "/projects")
        return result if isinstance(result, list) else []
    
    def find_project_by_name(self, name: str) -> Optional[dict]:
        """Find a project containing the given name"""
        projects = self.get_projects()
        for p in projects:
            if name.lower() in p.get("name", "").lower():
                return p
        return None
    
    def set_project(self, project_id: str) -> bool:
        """Set active project and retrieve latest commit"""
        self.project_id = project_id
        commits = self._request("GET", f"/projects/{project_id}/commits")
        
        if commits and isinstance(commits, list) and len(commits) > 0:
            self.commit_id = commits[-1].get("@id")
            return True
        
        print(f"[WARNING] No commits found for project {project_id}")
        return False
    
    # -------------------------------------------------------------------------
    # Element Operations (PIM-EN-001, PIM-EN-002)
    # -------------------------------------------------------------------------
    
    def query_by_name(self, name: str) -> Optional[dict]:
        """
        PIM-EN-001: Query element by name

        NOTE: Modified to use GET /elements instead of POST /query
        to avoid 405 errors with some SysML v2 API implementations.
        Filters elements by name client-side.
        """
        if not self.project_id or not self.commit_id:
            print("[ERROR] No project selected. Call set_project() first.")
            return None

        # Get all elements and filter by name
        all_elements = self.get_all_elements()

        if not all_elements:
            print(f"[WARNING] No elements found in project")
            return None

        # Search for element with matching name
        for element in all_elements:
            if element.get("name") == name:
                return element

        # If exact match not found, try case-insensitive match
        for element in all_elements:
            if element.get("name", "").lower() == name.lower():
                print(f"[INFO] Found '{element.get('name')}' (case-insensitive match)")
                return element

        return None
    
    def get_element(self, element_id: str) -> Optional[dict]:
        """PIM-EN-002: Get element by ID"""
        if not self.project_id or not self.commit_id:
            return None
        
        # Check cache first
        cache_key = f"{self.commit_id}:{element_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        result = self._request(
            "GET",
            f"/projects/{self.project_id}/commits/{self.commit_id}/elements/{element_id}"
        )
        
        if result:
            self._cache[cache_key] = result
        
        return result
    
    def get_all_elements(self) -> List[dict]:
        """Get all elements in current commit"""
        if not self.project_id or not self.commit_id:
            return []
        
        result = self._request(
            "GET",
            f"/projects/{self.project_id}/commits/{self.commit_id}/elements"
        )
        
        return result if isinstance(result, list) else []
    
    # -------------------------------------------------------------------------
    # Parameter Extraction (Based on paper's Code (4))
    # -------------------------------------------------------------------------
    
    def extract_parameters(self, part_name: str) -> Dict[str, Any]:
        """
        Extract all parameters from a part as key-value dict
        
        This is the core function from the paper that traverses the
        model tree to find literal values.
        
        Args:
            part_name: Name of the part (e.g., "fourCylinderEngine")
            
        Returns:
            Dict mapping attribute names to their values
            e.g., {"mass": 120, "bore": 86, ...}
        """
        part = self.query_by_name(part_name)
        if not part:
            print(f"[WARNING] Part '{part_name}' not found")
            return {}
        
        return self._extract_values(part["@id"], {})
    
    def _extract_values(self, element_id: str, 
                        values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively extract literal values from an element
        Adapted from paper's get_value_for_attribute (Code (4))
        """
        element = self.get_element(element_id)
        if not element:
            return values
        
        name = element.get("name", "")
        members = element.get("member", [])
        
        for member in members:
            member_id = member.get("@id")
            if not member_id:
                continue
            
            member_data = self.get_element(member_id)
            if not member_data:
                continue
            
            member_type = member_data.get("@type", "")
            
            # Recurse into nested parts and attributes
            if member_type in ["AttributeUsage", "ItemUsage", "PartUsage"]:
                self._extract_values(member_id, values)
            
            # Extract literal values from operator expressions
            elif member_type == "OperatorExpression":
                arguments = member_data.get("argument", [])
                for arg in arguments:
                    arg_data = self.get_element(arg.get("@id"))
                    if arg_data and arg_data.get("@type") in [
                        "LiteralInteger", "LiteralReal", "LiteralString"
                    ]:
                        if name:  # Only record if we have an attribute name
                            values[name] = arg_data.get("value")
            
            # Direct literal values
            elif member_type in ["LiteralInteger", "LiteralReal"]:
                if name:
                    values[name] = member_data.get("value")
        
        return values
    
    # -------------------------------------------------------------------------
    # Commit Operations (PIM-PCB-010)
    # -------------------------------------------------------------------------
    
    def create_commit(self, changes: List[dict]) -> Optional[dict]:
        """
        PIM-PCB-010: Create a commit with changes
        
        Args:
            changes: List of element payloads to commit
            
        Returns:
            Commit result or None on failure
        """
        if not self.project_id:
            return None
        
        commit_body = {
            "@type": "Commit",
            "change": [
                {
                    "@type": "DataVersion",
                    "payload": change
                }
                for change in changes
            ]
        }
        
        result = self._request(
            "POST",
            f"/projects/{self.project_id}/commits",
            commit_body
        )
        
        if result:
            # Update current commit ID
            self.commit_id = result.get("@id")
        
        return result


# ============================================================================
# FUSION 360 PARAMETER BRIDGE
# ============================================================================

class FusionParameterBridge:
    """
    Bridge between SysML v2 parameters and Fusion 360 parameters
    
    Handles:
    - Parameter mapping based on @FusionParameter metadata
    - Unit conversions
    - Sync direction filtering
    """
    
    def __init__(self, client: SysMLv2Client):
        self.client = client
        self.parameter_map = PARAMETER_MAP
    
    def get_fusion_parameters(self, part_name: str, 
                              direction: str = "toFusion") -> Dict[str, dict]:
        """
        Extract parameters formatted for Fusion 360
        
        Args:
            part_name: SysML part name (e.g., "fourCylinderEngine")
            direction: Filter by sync direction ("toFusion", "fromFusion", "both")
            
        Returns:
            Dict with Fusion parameter names as keys:
            {
                "bore_diameter": {
                    "value": 86,
                    "unit": "mm",
                    "sysml_name": "bore",
                    "direction": "toFusion"
                }
            }
        """
        sysml_params = self.client.extract_parameters(part_name)
        fusion_params = {}
        
        for sysml_name, value in sysml_params.items():
            if sysml_name in self.parameter_map:
                fusion_name, sync_dir, param_type, unit = self.parameter_map[sysml_name]
                
                # Filter by direction
                if direction == "all" or sync_dir == direction or sync_dir == "both":
                    fusion_params[fusion_name] = {
                        "value": value,
                        "unit": unit,
                        "sysml_name": sysml_name,
                        "direction": sync_dir,
                        "type": param_type
                    }
        
        return fusion_params
    
    def generate_fusion_script(self, part_name: str) -> str:
        """
        Generate Fusion 360 Python API code to set parameters
        
        Returns executable Python code for Fusion 360 scripting environment
        """
        params = self.get_fusion_parameters(part_name, direction="toFusion")
        
        if not params:
            return "# No parameters to set"
        
        lines = [
            "# Auto-generated from SysML v2 model (OttoEngine)",
            "# Run this in Fusion 360 Scripts and Add-Ins",
            "",
            "import adsk.core",
            "import adsk.fusion",
            "",
            "def run(context):",
            "    app = adsk.core.Application.get()",
            "    design = adsk.fusion.Design.cast(app.activeProduct)",
            "    if not design:",
            "        app.userInterface.messageBox('No active design')",
            "        return",
            "",
            "    userParams = design.userParameters",
            "    updates = []",
            "",
        ]
        
        for fusion_name, data in params.items():
            value = data["value"]
            unit = data["unit"]
            sysml_name = data["sysml_name"]
            
            # Handle different value types
            if unit and unit != "":
                value_str = f'"{value} {unit}"'
            else:
                value_str = f'"{value}"'
            
            lines.extend([
                f"    # {sysml_name} -> {fusion_name}",
                f"    param = userParams.itemByName('{fusion_name}')",
                f"    if param:",
                f"        param.expression = {value_str}",
                f"        updates.append('{fusion_name}')",
                f"    else:",
                f"        valueInput = adsk.core.ValueInput.createByString({value_str})",
                f"        userParams.add('{fusion_name}', valueInput, '{unit}', 'From SysML: {sysml_name}')",
                f"        updates.append('{fusion_name} (created)')",
                "",
            ])
        
        lines.extend([
            "    if updates:",
            "        app.userInterface.messageBox(",
            "            f'Updated {len(updates)} parameters:\\n' + '\\n'.join(updates))",
        ])
        
        return "\n".join(lines)


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="SysML v2 to Fusion 360 Bridge (OttoEngine Model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --test-connection
  %(prog)s --list-projects  
  %(prog)s --extract fourCylinderEngine
  %(prog)s --extract fourCylinderEngine --generate-fusion-script
  %(prog)s --host http://localhost:9000 --list-projects
        """
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=f"SysML v2 API server URL (default: {DEFAULT_HOST})"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test connection to SysML v2 API server"
    )
    
    parser.add_argument(
        "--list-projects",
        action="store_true",
        help="List all projects in repository"
    )
    
    parser.add_argument(
        "--project",
        help="Project name or ID to use"
    )
    
    parser.add_argument(
        "--extract",
        metavar="PART_NAME",
        help="Extract parameters from a part (e.g., fourCylinderEngine)"
    )
    
    parser.add_argument(
        "--list-elements",
        action="store_true",
        help="List all elements in the project"
    )
    
    parser.add_argument(
        "--generate-fusion-script",
        action="store_true",
        help="Generate Fusion 360 Python script (use with --extract)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    # Initialize client
    client = SysMLv2Client(args.host)
    
    # Test connection
    if args.test_connection:
        print(f"Testing connection to {args.host}...")
        projects = client.get_projects()
        if projects is not None:
            print(f"[OK] Connected! Found {len(projects)} project(s)")
            return 0
        else:
            print("[ERROR] Connection failed")
            return 1
    
    # List projects
    if args.list_projects:
        projects = client.get_projects()
        
        if not projects:
            print("No projects found (or API unavailable)")
            return 1
        
        if args.json:
            print(json.dumps(projects, indent=2))
        else:
            print(f"\nFound {len(projects)} project(s):\n")
            for p in projects:
                print(f"  [PROJECT] {p.get('name', 'Unnamed')}")
                print(f"     ID: {p.get('@id', 'N/A')}")
                print(f"     Description: {p.get('description', '-')}")
                print()
        return 0
    
    # Extract parameters
    if args.extract:
        # Find and set project
        if args.project:
            project = client.find_project_by_name(args.project)
        else:
            # Try to find OttoEngine project
            project = client.find_project_by_name("OttoEngine")
            if not project:
                # Use first available project
                projects = client.get_projects()
                project = projects[0] if projects else None
        
        if not project:
            print("[ERROR] No project found. Use --project to specify or --list-projects to see available.")
            return 1
        
        print(f"Using project: {project.get('name')}")
        client.set_project(project["@id"])
        
        # Extract parameters
        params = client.extract_parameters(args.extract)
        
        if not params:
            print(f"[WARNING] No parameters found for '{args.extract}'")
            print("\nTip: Try these element names from your model:")
            print("  - fourCylinderEngine  (main engine instance)")
            print("  - OttoEngine          (engine definition)")
            print("  - Piston              (piston definition)")
            print("  - Cylinder            (cylinder definition)")
            print("  - ConnectingRod       (connecting rod definition)")
            print("  - Crankshaft          (crankshaft definition)")
            return 1
        
        if args.generate_fusion_script:
            bridge = FusionParameterBridge(client)
            script = bridge.generate_fusion_script(args.extract)

            # Generate filename based on part name
            script_filename = f"fusion_script_{args.extract}.py"
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_filename)

            # Write script to file
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script)

            print(f"\n[SUCCESS] Fusion 360 script generated!")
            print(f"   File: {script_filename}")
            print(f"   Path: {script_path}")
            print(f"\nTo use in Fusion 360:")
            print(f"   1. Open Fusion 360")
            print(f"   2. Go to Tools > Scripts and Add-Ins > Scripts tab")
            print(f"   3. Click the '+' icon and select this file")
            print(f"   4. Select the script and click 'Run'")
        elif args.json:
            print(json.dumps(params, indent=2))
        else:
            print(f"\nExtracted {len(params)} parameters from '{args.extract}':\n")
            
            # Group by mapping status
            mapped = {}
            unmapped = {}
            
            for name, value in params.items():
                if name in PARAMETER_MAP:
                    fusion_name, direction, _, unit = PARAMETER_MAP[name]
                    mapped[name] = {
                        "value": value,
                        "fusion_name": fusion_name,
                        "direction": direction,
                        "unit": unit
                    }
                else:
                    unmapped[name] = value
            
            if mapped:
                print("[MAPPED] Mapped to Fusion parameters:")
                for name, data in sorted(mapped.items()):
                    dir_icon = "->" if data["direction"] == "toFusion" else "<-" if data["direction"] == "fromFusion" else "<->"
                    unit = f" {data['unit']}" if data['unit'] else ""
                    print(f"   {name}: {data['value']}{unit}")
                    print(f"      {dir_icon} {data['fusion_name']}")
                print()
            
            if unmapped:
                print("[UNMAPPED] Additional parameters (not mapped):")
                for name, value in sorted(unmapped.items()):
                    print(f"   {name}: {value}")
        
        return 0
    
    # List elements
    if args.list_elements:
        # Find project first
        if args.project:
            project = client.find_project_by_name(args.project)
        else:
            projects = client.get_projects()
            project = projects[0] if projects else None
        
        if not project:
            print("[ERROR] No project found")
            return 1
        
        client.set_project(project["@id"])
        elements = client.get_all_elements()
        
        if args.json:
            print(json.dumps(elements, indent=2))
        else:
            # Filter to show useful elements
            parts = [e for e in elements if e.get("@type") in 
                    ["PartDefinition", "PartUsage", "Package"]]
            
            print(f"\nFound {len(parts)} parts/packages in '{project.get('name')}':\n")
            for e in parts[:50]:  # Limit output
                etype = e.get("@type", "").replace("Definition", " def").replace("Usage", "")
                print(f"   [{etype:15}] {e.get('name', 'Unnamed')}")
            
            if len(parts) > 50:
                print(f"\n   ... and {len(parts) - 50} more")
        
        return 0
    
    # No command specified
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
