"""
This module contains a list of utilities related to validation of command line arguments received from user.
"""

import framework.utils.constants as constants
import framework.utils.android as android
import framework.utils.ios as ios
import argparse
import os


def connected_device(given_device):
    """
    Validates given connected device.

    :param given_device Given device name
    """
    devices = android.list_devices() + ios.list_devices()
    if not devices:
        raise argparse.ArgumentTypeError("No connected devices")
    if given_device is not None and given_device not in devices:
        raise argparse.ArgumentTypeError("Unknown device")
    if given_device is None and len(devices) > 1:
        raise argparse.ArgumentTypeError("More than one device")
    return given_device


def connected_android_device(given_device):
    """
    Validates given connected android device.

    :param given_device Given device name
    """
    devices = android.list_devices()
    if not devices:
        raise argparse.ArgumentTypeError("No connected Android devices")
    if given_device is not None and given_device not in devices:
        raise argparse.ArgumentTypeError("Unknown Android device")
    if given_device is None and len(devices) > 1:
        raise argparse.ArgumentTypeError("More than one Android device")
    return given_device


def existent_file(file_path):
    """
    Validates if given file exists.

    :param file_path Absolute path to file
    """
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError("Input file path does not exist")
    return file_path


def supported_platform(given_platform):
    """
    Validates if given platform is correct.

    :param given_platform: string, Platform name.
    """
    if given_platform not in constants.platforms():
        raise argparse.ArgumentTypeError("Invalid platform given: " + given_platform)
    return given_platform


def log_level(given_level):
    """
    Validates if given logs level is correct.

    :param given_level Provided log level
    """
    if given_level not in constants.log_levels():
        raise argparse.ArgumentTypeError("Invalid log level given: " + given_level)
    return given_level


def adb_video_limit(given_limit):
    """
    Validates if given ADB bitrate is correct or not.

    :param given_limit: int, given video limit, seconds.
    :returns limit: int, validated video limit.
    """
    return given_limit


def valid_state(given_state):
    """
    Validates if given state is either ON or OFF.

    :param given_state Provided state.
    """
    if given_state not in ["ON", "OFF"]:
        raise argparse.ArgumentTypeError("Invalid state given: " + given_state)
    return given_state
