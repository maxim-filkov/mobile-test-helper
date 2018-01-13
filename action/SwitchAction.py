"""
This module contains a list of actions related to switching ON/OFF different functions on mobile devices, e.g. WiFi.
"""

import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
from action.ActionFactory import ActionFactory
import framework.utils.android as android
import logging
import sys

log = logging.getLogger("action")


class SwitchAction(object):
    """
    Actions for switching ON/OFF different functions on mobile devices.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
            Meta class to describe action.
            """
        action = "switch"
        help = "A set of utils to switch ON/OFF functions on mobile devices"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        subparsers = parser.add_subparsers(title="Switch ON/OFF actions",
                                           dest="switch",
                                           help="List of actions to switch ON/OFF")

        parser = subparsers.add_parser("wifi", help="Switch ON/OFF wifi")
        SwitchAction._init_parser(parser)

        parser = subparsers.add_parser("cellular", help="Switch ON/OFF cellular")
        SwitchAction._init_parser(parser)

    def __call__(self, **kwargs):
        subaction = kwargs[SwitchAction.Meta.action]
        del kwargs[SwitchAction.Meta.action]

        if subaction == "wifi":
            android.switch_wifi(**kwargs)
        elif subaction == "cellular":
            android.switch_cellular_data(**kwargs)
        else:
            log.error("Unknown subcommand given: '{0}'".format(subaction))
            sys.exit(1)

    @staticmethod
    def _init_parser(parser):
        parser.add_argument("-", "--device",
                            help="Device identifier",
                            type=types.connected_android_device,
                            default=defaults.connected_android_device()).completer = completion.android_devices
        parser.add_argument("-s", "--state",
                            help="ON to enable, OFF to disable",
                            required=True,
                            type=types.valid_state).completer = completion.onoff
