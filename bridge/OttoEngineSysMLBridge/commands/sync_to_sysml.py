"""
Sync To SysML Command

Pushes parameters from Fusion 360 to SysML v2 model.
"""

import adsk.core
import adsk.fusion
import traceback
import json
import os

# Add parent directory to path to import lib modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lib.sysml_api import SysMLv2Client
from lib.parameter_mapper import ParameterMapper

# Global variables
_app = None
_ui = None
_handlers = []


class SyncToSysMLCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Handler for command execution"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Get the command inputs
            inputs = args.command.commandInputs
            part_name_input = inputs.itemById('part_name')
            part_name = part_name_input.value

            # Get active design
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                _ui.messageBox("No active design found.", "Error")
                return

            # Load configuration
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config.json'
            )

            with open(config_path, 'r') as f:
                config = json.load(f)

            # Get parameters to sync
            mapper = ParameterMapper(design)
            fusion_to_sysml_params = mapper.sync_to_sysml(direction="fromFusion")

            if not fusion_to_sysml_params:
                _ui.messageBox(
                    "No parameters configured for sync to SysML.\n"
                    "Check that you have parameters with 'fromFusion' or 'both' direction.",
                    "No Parameters to Sync"
                )
                return

            # Connect to SysML API
            client = SysMLv2Client(config['sysml_api']['host'])

            # Find and set project
            project = client.find_project_by_name(config['sysml_api']['project_name'])
            if not project:
                _ui.messageBox(
                    f"Project '{config['sysml_api']['project_name']}' not found.\n"
                    "Check config.json and ensure the SysML API server is running.",
                    "Project Not Found"
                )
                return

            client.set_project(project['@id'])

            # NOTE: This is a placeholder for actual SysML update logic
            # The SysML v2 API for updating parameter values would need to be implemented
            # based on the specific API version and model structure

            # Show what would be synced
            message = f"Would sync {len(fusion_to_sysml_params)} parameters to SysML part '{part_name}':\n\n"
            for param_name, value in fusion_to_sysml_params.items():
                message += f"• {param_name}: {value}\n"

            message += "\n[NOTE] Actual SysML commit implementation pending.\n"
            message += "Requires SysML v2 API update methods for your model structure."

            _ui.messageBox(message, "Sync Preview")

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


class SyncToSysMLCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler for command creation"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            cmd.isExecutedWhenPreEmpted = False

            # Create command inputs
            inputs = cmd.commandInputs

            # Load config to get default part name
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config.json'
            )

            default_part = "fourCylinderEngine"
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    default_part = config['sysml_api'].get('default_part', default_part)
            except:
                pass

            # Add input for part name
            inputs.addStringValueInput(
                'part_name',
                'SysML Part Name',
                default_part
            )

            # Connect execute handler
            onExecute = SyncToSysMLCommandExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


def start():
    """Start the command"""
    global _app, _ui

    _app = adsk.core.Application.get()
    _ui = _app.userInterface

    # Get the CommandDefinitions collection
    cmdDefs = _ui.commandDefinitions

    # Create command definition
    cmdDef = cmdDefs.itemById('SyncToSysMLButton')
    if not cmdDef:
        cmdDef = cmdDefs.addButtonDefinition(
            'SyncToSysMLButton',
            'Sync To SysML',
            'Push parameters to SysML v2 model',
            './resources'
        )

    # Connect to command created event
    onCommandCreated = SyncToSysMLCommandCreatedHandler()
    cmdDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)

    # Execute the command
    cmdDef.execute()


def stop():
    """Stop the command"""
    global _ui

    # Clean up command definition
    _ui = adsk.core.Application.get().userInterface
    cmdDef = _ui.commandDefinitions.itemById('SyncToSysMLButton')
    if cmdDef:
        cmdDef.deleteMe()
