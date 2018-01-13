"""
This module contains list of utilities related to auto completion in console.
"""

import framework.utils.ios as ios
import framework.utils.android as android
from argcomplete import warn
import framework.utils.constants as constants


# noinspection PyUnusedLocal
def all_devices(prefix, parsed_args, **kwargs):
    """
    Returns all connected devices Android and iOS.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all connected devices.
    """
    devices = android.list_devices() + ios.list_devices()
    if not devices:
        warn("No connected devices")
    return devices


# noinspection PyUnusedLocal
def android_devices(prefix, parsed_args, **kwargs):
    """
    Returns all connected Android devices.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all connected Android devices.
    """
    devices = android.list_devices()
    if not devices:
        warn("No connected Android devices")
    return devices


# noinspection PyUnusedLocal
def ios_devices(prefix, parsed_args, **kwargs):
    """
    Returns all connected iOS devices.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all connected iOS devices.
    """
    devices = ios.list_devices()
    if not devices:
        warn("No connected iOS devices")
    return devices


# noinspection PyUnusedLocal
def supported_locales(prefix, parsed_args, **kwargs):
    """
    Returns all supported locales.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all supported locales.
    """
    return constants.locales()


# noinspection PyUnusedLocal
def log_levels(prefix, parsed_args, **kwargs):
    """
    Returns all supported log levels.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all supported log levels.
    """
    return constants.log_levels()


# noinspection PyUnusedLocal
def all_arm_architectures(prefix, parsed_args, **kwargs):
    """
    Returns all ARM architectures.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all ARM architectures.
    """
    return constants.arm_architectures()


# noinspection PyUnusedLocal
def truefalse(prefix, parsed_args, **kwargs):
    """
    Returns True and False.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: True and False.
    """
    return "True", "False"


# noinspection PyUnusedLocal
def all_platforms(prefix, parsed_args, **kwargs):
    """
    Returns all supported platforms.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: list of all supported platforms.
    """
    return constants.platforms()


# noinspection PyUnusedLocal
def onoff(prefix, parsed_args, **kwargs):
    """
    Returns ON and OFF.

    :param prefix: The prefix text of the last word before the cursor on the command line.
    :param parsed_args: The result of argument parsing so far.
    :param kwargs: keyword arguments.
    :returns list: ON and OFF.
    """
    return "ON", "OFF"
