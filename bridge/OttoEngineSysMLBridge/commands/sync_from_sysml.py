"""
Sync From SysML Command

Pulls parameters from SysML v2 model and updates Fusion 360 user parameters.
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


class SyncFromSysMLCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Handler for command execution"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Get the command inputs
            inputs = args.command.commandInputs
            part_name_input = inputs.itemById('part_name')
            part_name = part_name_input.value

            # Load configuration
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config.json'
            )

            with open(config_path, 'r') as f:
                config = json.load(f)

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

            # Extract parameters from SysML
            sysml_params = client.extract_parameters(part_name)

            if not sysml_params:
                _ui.messageBox(
                    f"No parameters found for part '{part_name}'.\n"
                    "Check that the part name is correct in your SysML model.",
                    "No Parameters Found"
                )
                return

            # Get active design
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                _ui.messageBox("No active design found.", "Error")
                return

            # Sync parameters
            mapper = ParameterMapper(design)
            updates = mapper.sync_from_sysml(sysml_params, direction="toFusion")

            # Show results
            if updates:
                message = f"Successfully synced {len(updates)} parameters from SysML:\n\n"
                for param_name, status in updates.items():
                    message += f"• {param_name}: {status}\n"

                _ui.messageBox(message, "Sync Complete")
            else:
                _ui.messageBox("No parameters were updated.", "Sync Complete")

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


class SyncFromSysMLCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
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
            onExecute = SyncFromSysMLCommandExecuteHandler()
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
    cmdDef = cmdDefs.itemById('SyncFromSysMLButton')
    if not cmdDef:
        cmdDef = cmdDefs.addButtonDefinition(
            'SyncFromSysMLButton',
            'Sync From SysML',
            'Pull parameters from SysML v2 model',
            './resources'
        )

    # Connect to command created event
    onCommandCreated = SyncFromSysMLCommandCreatedHandler()
    cmdDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)

    # Execute the command
    cmdDef.execute()


def stop():
    """Stop the command"""
    global _ui

    # Clean up command definition
    _ui = adsk.core.Application.get().userInterface
    cmdDef = _ui.commandDefinitions.itemById('SyncFromSysMLButton')
    if cmdDef:
        cmdDef.deleteMe()
