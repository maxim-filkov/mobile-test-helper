"""
This module contains actions related to locale.
"""

import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
from action.ActionFactory import ActionFactory
import framework.utils.console as console
import framework.utils.android as android
import logging

log = logging.getLogger("action")


class LocaleAction(object):
    """
    Action to set locale.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
        Meta class to describe action.
        """
        action = "locale"
        help = "Set locale on device"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        parser.add_argument("--device",
                            help="Device to set locale on",
                            type=types.connected_android_device,
                            default=defaults.connected_android_device()).completer = completion.android_devices
        parser.add_argument("--locale",
                            help="Locale to set on the device",
                            required=True).completer = completion.supported_locales

    def __call__(self, device, locale):
        """
        Sets a locale on the specified device.

        :param device: string, device identifier (e.g. "TA9890AMTG").
        :param locale: string, locale to set (e.g. "ru-RU").
        """
        if device is None:
            devices = android.list_devices()
            if devices:
                device = console.prompt_for_options("Please define exact device: ", devices)
            else:
                log.error("No connected Android devices")
                return 1
        android.set_locale(device, locale)
