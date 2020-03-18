"""
This module contains a list of actions related to logging.
"""

import logging
import sys

import framework.utils.android as android
import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
import framework.utils.console as console
import framework.utils.ios as ios
from action.ActionFactory import ActionFactory

log = logging.getLogger("action")


class LoggingAction(object):
    """
    Actions for logging.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
        Meta class to describe action.
        """
        action = "logging"
        help = "A set of functions related to logs"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        subparsers = parser.add_subparsers(title="Logging actions",
                                           dest="logging",
                                           help="List of available actions for logging")

        parser = subparsers.add_parser("start", help="Start logging process")
        LoggingAction._init_start_parser(parser)

    def __call__(self, **kwargs):
        subaction = kwargs[LoggingAction.Meta.action]
        del kwargs[LoggingAction.Meta.action]

        if subaction == "start":
            device = kwargs["device"]
            if device is None:
                devices = android.list_devices() + ios.list_devices()
                device = console.prompt_for_options("Choose device: ", devices)
            log_file = android.get_log(device) if device in android.list_devices() else ios.get_log(device)
            log.info("\nFind log at " + log_file)
        else:
            log.error("Unknown subcommand given: '{0}'".format(subaction))
            sys.exit(1)

    @staticmethod
    def _init_parse_parser(parser):
        parser.add_argument("-l", "--log-file",
                            help="Input log file that contains some crashes",
                            required=True,
                            type=types.existent_file)
        parser.add_argument("-o", "--out-file",
                            help="Specify output file, defaults to current directory")

    @staticmethod
    def _init_start_parser(parser):
        parser.add_argument("-d", "--device",
                            help="Device to get log from",
                            type=types.connected_device,
                            default=defaults.connected_device()).completer = completion.all_devices
