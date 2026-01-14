"""
OttoEngineSysMLBridge Add-In

Fusion 360 add-in for bidirectional parameter synchronization with SysML v2 models.

Based on: "Praktische Anwendung der SysML v2 API am Beispiel von MCAD und Simulation"
          (Manoury & Muggeo, TdSE 2023)

Features:
- Pull parameters from SysML v2 model to Fusion 360
- Push parameters from Fusion 360 to SysML v2 model
- Configurable parameter mappings
- Support for multiple sync directions (toFusion, fromFusion, both)
"""

import adsk.core
import adsk.fusion
import traceback
import sys
import os

# Add commands directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'commands'))

# Import command modules
from commands import sync_from_sysml
from commands import sync_to_sysml

# Global variables
_app = None
_ui = None
_handlers = []

# Panel and controls
PANEL_ID = 'SysMLBridgePanel'
CMD_SYNC_FROM_ID = 'SyncFromSysMLButton'
CMD_SYNC_TO_ID = 'SyncToSysMLButton'


def run(context):
    """
    Called when the add-in is started (run).
    Creates UI elements and registers commands.
    """
    global _app, _ui

    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Get the ADD-INS panel in the model workspace
        workspaces = _ui.workspaces
        modelingWorkspace = workspaces.itemById('FusionSolidEnvironment')
        toolbarPanels = modelingWorkspace.toolbarPanels

        # Create a new panel for SysML Bridge
        panel = toolbarPanels.itemById(PANEL_ID)
        if not panel:
            panel = toolbarPanels.add(PANEL_ID, 'SysML Bridge', 'SelectPanel', False)

        # Get command definitions
        cmdDefs = _ui.commandDefinitions

        # Create "Sync From SysML" button
        syncFromBtn = cmdDefs.itemById(CMD_SYNC_FROM_ID)
        if not syncFromBtn:
            syncFromBtn = cmdDefs.addButtonDefinition(
                CMD_SYNC_FROM_ID,
                'Sync From SysML',
                'Pull parameters from SysML v2 model and update Fusion 360 parameters',
                './resources'
            )

        # Create "Sync To SysML" button
        syncToBtn = cmdDefs.itemById(CMD_SYNC_TO_ID)
        if not syncToBtn:
            syncToBtn = cmdDefs.addButtonDefinition(
                CMD_SYNC_TO_ID,
                'Sync To SysML',
                'Push Fusion 360 parameters to SysML v2 model',
                './resources'
            )

        # Add buttons to panel
        syncFromControl = panel.controls.itemById(CMD_SYNC_FROM_ID)
        if not syncFromControl:
            syncFromControl = panel.controls.addCommand(syncFromBtn)
            syncFromControl.isPromoted = True
            syncFromControl.isPromotedByDefault = True

        syncToControl = panel.controls.itemById(CMD_SYNC_TO_ID)
        if not syncToControl:
            syncToControl = panel.controls.addCommand(syncToBtn)
            syncToControl.isPromoted = True
            syncToControl.isPromotedByDefault = True

        # Connect command created events
        onSyncFromCreated = SyncFromSysMLCreatedHandler()
        syncFromBtn.commandCreated.add(onSyncFromCreated)
        _handlers.append(onSyncFromCreated)

        onSyncToCreated = SyncToSysMLCreatedHandler()
        syncToBtn.commandCreated.add(onSyncToCreated)
        _handlers.append(onSyncToCreated)

        _ui.messageBox('OttoEngineSysMLBridge add-in loaded successfully.\n\n'
                      'Look for the "SysML Bridge" panel in your toolbar.')

    except Exception as e:
        if _ui:
            _ui.messageBox(f'Failed to start add-in:\n{traceback.format_exc()}')


def stop(context):
    """
    Called when the add-in is stopped.
    Cleans up UI elements and handlers.
    """
    global _ui

    try:
        _ui = adsk.core.Application.get().userInterface

        # Remove panel
        workspaces = _ui.workspaces
        modelingWorkspace = workspaces.itemById('FusionSolidEnvironment')
        toolbarPanels = modelingWorkspace.toolbarPanels
        panel = toolbarPanels.itemById(PANEL_ID)
        if panel:
            panel.deleteMe()

        # Remove command definitions
        cmdDefs = _ui.commandDefinitions
        syncFromBtn = cmdDefs.itemById(CMD_SYNC_FROM_ID)
        if syncFromBtn:
            syncFromBtn.deleteMe()

        syncToBtn = cmdDefs.itemById(CMD_SYNC_TO_ID)
        if syncToBtn:
            syncToBtn.deleteMe()

        _ui.messageBox('OttoEngineSysMLBridge add-in stopped.')

    except Exception as e:
        if _ui:
            _ui.messageBox(f'Failed to stop add-in:\n{traceback.format_exc()}')


class SyncFromSysMLCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler for Sync From SysML command creation"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            onExecute = SyncFromSysMLExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

            # Create command inputs
            inputs = cmd.commandInputs

            # Add part name input
            inputs.addStringValueInput(
                'part_name',
                'SysML Part Name',
                'fourCylinderEngine'
            )

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


class SyncFromSysMLExecuteHandler(adsk.core.CommandEventHandler):
    """Handler for Sync From SysML command execution"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Delegate to command module
            sync_from_sysml.start()

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


class SyncToSysMLCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler for Sync To SysML command creation"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            onExecute = SyncToSysMLExecuteHandler()
            cmd.execute.add(onExecute)
            _handlers.append(onExecute)

            # Create command inputs
            inputs = cmd.commandInputs

            # Add part name input
            inputs.addStringValueInput(
                'part_name',
                'SysML Part Name',
                'fourCylinderEngine'
            )

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')


class SyncToSysMLExecuteHandler(adsk.core.CommandEventHandler):
    """Handler for Sync To SysML command execution"""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            # Delegate to command module
            sync_to_sysml.start()

        except Exception as e:
            _ui.messageBox(f'Failed:\n{traceback.format_exc()}')
