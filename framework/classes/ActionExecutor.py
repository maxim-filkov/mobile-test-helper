"""
This module contains ActionExecutor - class that is responsible for executing actions.
"""

from action.ActionRegistry import ActionRegistry


class ActionExecutor(object):
    """
    Executes actions received from registry.
    """

    def __call__(self, cmd):
        action = cmd.action
        delattr(cmd, 'action')
        return ActionRegistry.registry[action]()(**vars(cmd))
