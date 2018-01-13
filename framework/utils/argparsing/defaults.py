"""
This module contains a list of utilities related to getting default values for different command line parameters.
"""

import framework.utils.android as android
import framework.utils.ios as ios
import logging
import os

log = logging.getLogger("utils")


def connected_device():
    """
    Discovers and returns connected device.

    :returns string: connected device Android or iOS (if single).
    """
    devices = android.list_devices() + ios.list_devices()
    if not devices or len(devices) > 1:
        return None
    return devices[0]


def connected_android_device():
    """
    Discovers and returns connected android device.

    :returns string: connected Android device (if single).
    """
    devices = android.list_devices()
    if not devices or len(devices) > 1:
        return None
    return devices[0]


def current_directory():
    """
    Returns current directory, if not writable when user home directory.

    :returns string: current directory path.
    """
    current_dir = os.getcwd()
    return current_dir if os.access(current_dir, os.W_OK) else os.path.expanduser('~')
