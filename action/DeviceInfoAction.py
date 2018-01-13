"""
This module contains actions related to getting info about connected mobile devices.
"""

import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
from action.ActionFactory import ActionFactory
import framework.utils.android as android
import framework.utils.ios as ios
import logging
import sys

log = logging.getLogger("action")


class DeviceInfoAction(object):
    """
    Action to get info about connected devices.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
        Meta class to describe action.
        """
        action = "devices"
        help = "Get info about connected devices"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        parser.add_argument("-d", "--device",
                            help="Optional, Device to get info, by default all connected devices",
                            type=types.connected_device,
                            default=defaults.connected_device()).completer = completion.all_devices
        parser.add_argument("-p", "--platform",
                            help="Optional, Platform (android or ios) to get info, by default all platforms",
                            type=types.supported_platform,
                            default=None).completer = completion.all_platforms
        parser.add_argument("-hw", "--hardware",
                            help="Optional, If only hardware info is needed, by default all info",
                            action="store_true",
                            default=False)
        parser.add_argument("-sw", "--software",
                            help="Optional, If only software info is needed, by default all info",
                            action="store_true",
                            default=False)

    def __call__(self, device, platform, hardware, software):
        """
        Prints info for the given device or for all (if device is not specified).

        :param device: string, device identifier (e.g. "TA9890AMTG").
        :param hardware: boolean, True if only hardware info is needed, otherwise False.
        :param software: boolean, True if only software info is needed, otherwise False.
        """
        android_devices = android.list_devices()
        ios_devices = ios.list_devices()
        if device is None:
            devices = android_devices + ios_devices
            if not devices:
                log.error("No connected devices")
                sys.exit(1)

        show_hardware = hardware or (not hardware and not software)
        show_software = software or (not hardware and not software)

        for device in android_devices:
            if platform and platform != "android":
                break
            log.info("\nAndroid device: {0} ({1} {2})".format(device, android.get_manufacturer(device),
                                                              android.get_device_model(device)))
            if show_software:
                log.info("Android version: {0}".format(android.get_android_version(device)))
            if show_hardware:
                log.info("CPU frequency: {0}GHz".format(android.get_cpu_frequency(device)))
                log.info("RAM size: {0}GB".format(android.get_ram_size(device)))
                log.info("Screen resolution: {0}".format(android.get_resolution(device)))
                log.info("SDK version: {0}".format(android.get_sdk_version(device)))
                log.info("IP address: {0}".format(android.get_ip_address(device)))

        for device in ios_devices:
            if platform and platform != "ios":
                break
            log.info("\niOS device: {0} ({1})".format(device, ios.get_device_model(device)))
