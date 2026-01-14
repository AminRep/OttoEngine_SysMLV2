"""
Diagnostic version to test imports
"""

import adsk.core
import adsk.fusion
import traceback
import sys
import os

_app = None
_ui = None

def run(context):
    """Test which imports fail"""
    global _app, _ui

    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        _ui.messageBox('Step 1: Basic imports OK')

        # Test sys.path modification
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'commands'))
        _ui.messageBox(f'Step 2: Path added\n{os.path.dirname(__file__)}')

        # Test typing import
        try:
            from typing import Dict, List, Optional, Any
            _ui.messageBox('Step 3: typing import OK')
        except Exception as e:
            _ui.messageBox(f'Step 3 FAILED: typing import\n{str(e)}')
            return

        # Test lib imports
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
            from lib import sysml_api
            _ui.messageBox('Step 4: lib.sysml_api import OK')
        except Exception as e:
            _ui.messageBox(f'Step 4 FAILED: lib.sysml_api\n{traceback.format_exc()}')
            return

        try:
            from lib import parameter_mapper
            _ui.messageBox('Step 5: lib.parameter_mapper import OK')
        except Exception as e:
            _ui.messageBox(f'Step 5 FAILED: lib.parameter_mapper\n{traceback.format_exc()}')
            return

        # Test command imports
        try:
            from commands import sync_from_sysml
            _ui.messageBox('Step 6: commands.sync_from_sysml import OK')
        except Exception as e:
            _ui.messageBox(f'Step 6 FAILED: commands.sync_from_sysml\n{traceback.format_exc()}')
            return

        try:
            from commands import sync_to_sysml
            _ui.messageBox('Step 7: commands.sync_to_sysml import OK')
        except Exception as e:
            _ui.messageBox(f'Step 7 FAILED: commands.sync_to_sysml\n{traceback.format_exc()}')
            return

        _ui.messageBox('ALL IMPORTS SUCCESSFUL!\nProblem is elsewhere.')

    except Exception as e:
        if _ui:
            _ui.messageBox(f'Diagnostic failed:\n{traceback.format_exc()}')

def stop(context):
    if _ui:
        _ui.messageBox('Diagnostic stopped')
