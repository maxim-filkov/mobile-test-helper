"""
This module contains actions related to taking screenshots from mobile devices.
"""

import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
from action.ActionFactory import ActionFactory
import framework.utils.android as android
import framework.utils.console as console
import framework.utils.ios as ios
import logging
import time
import sys
import os

log = logging.getLogger("action")


class TakeScreenshotAction(object):
    """
    Action for taking screenshots.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
        Meta class to describe action.
        """
        action = "screenshot"
        help = "Takes screenshots from device"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        parser.add_argument("--device",
                            help="Device to take screenshot from",
                            type=types.connected_device,
                            default=defaults.connected_device()).completer = completion.all_devices

        parser.add_argument("--howmany",
                            help="How many screenshots to take",
                            type=int,
                            default=1)

        parser.add_argument("--locales",
                            help="One or more locale to take screenshot for",
                            default=None,
                            nargs='+').completer = completion.supported_locales

    def __call__(self, device, howmany=1, **locales):
        """
        Takes one or more screenshots from specified device.

        :param device: string, device identifier (e.g. "TA9890AMTG").
        """
        locales = locales.values()[0]
        if device is None:
            devices = android.list_devices() + ios.list_devices()
            device = console.prompt_for_options("Choose device", devices)

        target_dir = os.getcwd()
        many_screenshots = howmany > 1 or (locales and len(locales) > 1)
        if many_screenshots:
            target_dir = os.path.join(target_dir, str(int(time.time() * 1000)))
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

        for i in range(0, howmany):
            if device in android.list_devices():
                model = android.get_device_model(device).lower().replace(" ", "")
                manufacturer = android.get_manufacturer(device).lower().replace(" ", "")
                timestamp = str(int(time.time() * 1000))
                screenshot_name = "{0}_{1}_{2}.png".format(model, manufacturer, timestamp)
                if locales:
                    locale_before = android.get_locale(device)
                    for locale in locales:
                        android.set_locale(device, locale)
                        android.take_screenshot(device, target_dir, locale + "_" + screenshot_name)
                    android.set_locale(device, locale_before)
                else:
                    android.take_screenshot(device, target_dir, screenshot_name)
            elif device in ios.list_devices():
                model = ios.get_device_model(device).lower().replace(" ", "")
                timestamp = str(int(time.time() * 1000))
                screenshot_name = "{0}_{1}.png".format(model, timestamp)
                ios.take_screenshot(device, target_dir, screenshot_name)
            else:
                log.error("Unknown device given: '{0}'", format(device))
                sys.exit(1)
        # noinspection PyUnboundLocalVariable
        log.info("Find result at " + (target_dir if many_screenshots else os.path.join(target_dir, screenshot_name)))
