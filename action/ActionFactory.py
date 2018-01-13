"""
This module contains ActionFactory class that creates action instances and saves them into registry.
"""

from ActionRegistry import ActionRegistry


class ActionFactory(type):
    """
    Populates registry with action instances.
    """

    def __init__(cls, classname, bases, dct):
        super(ActionFactory, cls).__init__(classname, bases, dct)
        # noinspection PyUnresolvedReferences
        ActionRegistry.registry[cls.Meta.action] = cls
