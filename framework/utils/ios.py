"""
This module contains a list of utilities related to iOS.
"""

import framework.utils.console as console
import logging
import string
import time
import os

log = logging.getLogger("mth.utils")


def take_screenshot(device, target_dir, screenshot_name):
    """
    Takes screenshot in .png format from attached iOS device.

    :param device: device identifier (e.g. "TA9890AMTG").
    :param target_dir: string, directory where to save screenshot.
    :param screenshot_name: string, screenshot name.
    """
    command = "idevicescreenshot -u " + device + " " + os.path.join(target_dir, screenshot_name)
    console.execute(command)


def get_ios_version(device):
    """
    Returns iOS version for specified device.

    :param device: device identifier, e.g. 860850006baba72f031cf22a333ba36d65239b61.
    :returns string: iOS version for specified device.
    """
    command = "ideviceinfo -u {0} -k ProductVersion".format(device)
    stdout = console.execute(command)
    return stdout


def list_devices():
    """
    Lists connected iOS devices.

    :returns: List of devices.
    """
    command = "idevice_id -l"
    stdout = console.execute(command)
    return filter(None, string.split(stdout, '\n'))


def get_log(device):
    """
    Gets log file from device.

    :param device: device identifier (e.g. "TA9890AMTG").
    """
    file_name = str(int(time.time() * 1000)) + ".txt"
    target_dir = os.getcwd()
    log_path = os.path.join(target_dir, file_name)
    device_time = get_time(device)[11:-13]
    get_log_command = "idevicesyslog -u {0}".format(device)
    log.info("Logging in progress to '" + log_path + "'... To finish press Ctrl+C")
    console.execute(get_log_command, False, log_path)
    return log_path


def get_time(device):
    """
    Returns current device time.

    :param device: device identifier (e.g. "TA9890AMTG").
    """
    command = "idevicedate -u " + device
    stdout = console.execute(command)
    return stdout


def get_xcode_version():
    """
    :returns string: Current installed Xcode version.
    """
    return console.execute("xcodebuild -version").split()[1]


def install_app(device, path):
    """
    Installs the application onto the given device. If not app is given, installs the very latest app from ~/Downloads.

    :param device: device identifier, e.g. "860850006baba72f031cf22a333ba36d65239b61".
    :param path: absolute path to .ipa file.
    """
    command = "ideviceinstaller -u {0} -g {1}".format(device, path)
    log.info("Installing '{0}' onto device '{1}'...".format(path, device))
    console.execute(command)


def uninstall_app(device, package):
    """
    Uninstalls given application by its package name.

    :param device: device identifier, e.g. "a4f9c477beb3096b8fbb86b58c23026d3da7756e".
    :param package: string, package name, e.g "com.android.calculator2".
    """
    command = "ideviceinstaller -u " + device + " -U " + package
    console.execute(command)


def get_device_model(device):
    """
    :param device: string, Device identifier.
    :returns string: Device model, e.g. "Motorola X2".
    """
    command = "ideviceinfo -u {0} -k ProductType".format(device)
    device_type = console.execute(command)
    return get_product_name(device_type)


def get_device_udid(device):
    """
    Returns Unique Device Identifier (UDID).

    :param device: device identifier.
    :returns string: UDID.
    """
    command = "ideviceinfo -u {0} -k UniqueDeviceID".format(device)
    return console.execute(command)


def is_app_installed(device, package):
    """
    Verifies if the given application is installed on the device.
    Returns all installed packages as a list.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param package: string, package name, e.g. "com.android.calculator2".
    :returns boolean: True if app is installed, otherwise False.
    """
    command = "ideviceinstaller -u {0} -l".format(device)
    stdout = console.execute(command)
    return package in stdout


def get_product_name(device_type):
    """
    Returns product name for iOS device by the given type.

    :param device_type: device type from ideviceinfo output, e.g. "iPhone4,1".
    :returns product_name: string, e.g. "iPhone 4s".
    """
    types2names = {
        "iPhone1,1": "iPhone",
        "iPhone1,2": "iPhone 3G",
        "iPhone2,1": "iPhone 3GS",
        "iPhone3,1": "iPhone 4 (GSM)",
        "iPhone3,3": "iPhone 4 (CDMA)",
        "iPhone4,1": "iPhone 4S",
        "iPhone5,1": "iPhone 5",
        "iPhone5,2": "iPhone 5",
        "iPhone5,3": "iPhone 5c",
        "iPhone5,4": "iPhone 5c",
        "iPhone6,1": "iPhone 5s",
        "iPhone6,2": "iPhone 5s",
        "iPhone7,1": "iPhone 6 Plus",
        "iPhone7,2": "iPhone 6",
        "iPhone8,1": "iPhone 6s",
        "iPad1,1": "iPad",
        "iPad2,1": "iPad 2 (Wi-Fi)",
        "iPad2,2": "iPad 2 (GSM)",
        "iPad2,3": "iPad 2 (CDMA)",
        "iPad2,4": "iPad 2 (Wi-Fi)",
        "iPad2,5": "iPad Mini (Wi-Fi)",
        "iPad2,6": "iPad Mini",
        "iPad2,7": "iPad Mini",
        "iPad3,1": "iPad 3 (Wi-Fi)",
        "iPad3,2": "iPad 3 (Wi-Fi+LTE Verizon)",
        "iPad3,3": "iPad 3 (Wi-Fi+LTE AT&T)",
        "iPad3,4": "iPad 4 (Wi-Fi)",
        "iPad3,5": "iPad 4",
        "iPad3,6": "iPad 4",
        "iPad4,1": "iPad Air (Wi-Fi)",
        "iPad4,2": "iPad Air (Wi-Fi+LTE)",
        "iPad4,3": "iPad Air (Rev)",
        "iPad4,4": "iPad Mini 2 (Wi-Fi)",
        "iPad4,5": "iPad Mini 2 (Wi-Fi+LTE)",
        "iPad4,6": "iPad Mini 2 (Rev)",
        "iPad4,7": "iPad Mini 3 (Wi-Fi)",
        "iPad4,8": "iPad Mini 3",
        "iPad4,9": "iPad Mini 3",
        "iPad5,3": "iPad Air 2 (Wi-Fi)",
        "iPad5,4": "iPad Air 2 (Wi-Fi+LTE)",
        "iPod1,1": "iPod Touch",
        "iPod2,1": "iPod Touch 2",
        "iPod3,1": "iPod Touch 3",
        "iPod4,1": "iPod Touch 4",
        "iPod5,1": "iPod Touch 5"
    }
    return types2names.get(device_type)
