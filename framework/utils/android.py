"""
This module contains a list of utilities related to Android.
"""

import framework.utils.console as console
import logging
import string
import glob
import time
import os
import re

log = logging.getLogger("mth.utils")


def take_screenshot(device, target_dir, screenshot_name):
    """
    Takes screenshot from attached Android device and saves this in specified folder.

    :param device: device identifier (e.g. "TA9890AMTG").
    :param target_dir: string, directory where to save screenshot.
    :param screenshot_name: string, screenshot name.
    """
    device_path = os.path.join("/sdcard/", screenshot_name)
    command = "adb -s " + device + " shell screencap -p " + device_path
    local_file = os.path.join(target_dir, screenshot_name)
    console.execute(command)
    download_file(device, device_path, local_file)
    remove_file(device, device_path)


def download_file(device, device_file_path, target_file_path):
    """
    Downloads file from attached Android device.

    :param device: string, unique identifier of device (optional, by default connected device).
    :param device_file_path: string, path to file that should be downloaded.
    :param target_file_path: path where to save the downloaded file.
    """
    command = "adb -s " + device + " pull " + device_file_path + " " + target_file_path
    console.execute(command)


def remove_file(device, device_file_path):
    """
    Removes file from attached Android device.

    :param device: string, unique identifier of device (optional, by default connected device).
    :param device_file_path: string, path to file that should be removed.
    """
    command = "adb -s " + device + " shell rm -f " + device_file_path
    console.execute(command)


def list_devices():
    """
    Lists connected android devices.
    """
    command = "adb devices"
    stdout = console.execute(command)
    lines = string.split(stdout, '\n')
    del lines[0]
    lines = filter(None, lines)
    devices = []
    for device in lines:
        devices.append(string.split(device, "\t")[0])
    return devices


def record_video(device, duration=180, bitrate=8000000):
    """
    Records video from attached Android device.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param duration: int, maximum duration for video, seconds.
    :param bitrate: int, video bit-rate, megabits per second.
    :returns string, recorded video file path on the device.
    """
    file_name = str(int(time.time() * 1000)) + ".mp4"
    device_path = os.path.join("/sdcard/", file_name)
    command = "/usr/local/bin/adb -s " + device + " shell screenrecord --time-limit " + \
              str(duration) + " --bit-rate " + str(bitrate) + " " + device_path
    log.info("Recording in progress... To finish press Ctrl+C")
    console.execute(command)
    time.sleep(1)
    return device_path


def get_log(device):
    """
    Gets log file from device.
    :param device: device identifier (e.g. "TA9890AMTG").
    """
    file_name = str(int(time.time() * 1000)) + ".txt"
    target_dir = os.getcwd()
    log_path = os.path.join(target_dir, file_name)
    clear_log_command = "adb -s " + device + " logcat -c"
    get_log_command = "adb -s " + device + " logcat -v time"
    console.execute(clear_log_command)
    log.info("Logging in progress to '" + log_path + "'... To finish press Ctrl+C")
    console.execute(get_log_command, False, log_path)
    return log_path


def get_locale(device):
    """
    Returns current locale for device.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :returns locale: string, locale set on the device, e.g. "en-US".
    """
    language_command = "adb -s {0} shell getprop persist.sys.language".format(device)
    country_command = "adb -s {0} shell getprop persist.sys.country".format(device)
    language = console.execute(language_command).rstrip()
    country = console.execute(country_command).rstrip()
    return language + "-" + country


def set_locale(device, locale):
    """
    Sets locale on device.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param locale: string, locale to set on the device, e.g. "en-US".
    """
    adbchangelanguage = "net.sanapeli.adbchangelanguage"

    language, country = string.split(locale, "-")
    command = "adb -s " + device + " shell am start -n net.sanapeli.adbchangelanguage/.AdbChangeLanguage " + \
              "-e language " + language + " -e country " + country
    if not _is_app_installed(device, adbchangelanguage):
        _open_google_play_for_app(device, adbchangelanguage)
        console.prompt("Please install adbchangelanguage then press Enter: ")
    _grant_permissions_to_change_config(device, adbchangelanguage)
    console.execute(command)
    time.sleep(3)


def install_app(device, app):
    """
    Installs the application onto the given device. If no app is given, installs the very latest app from ~/Downloads.

    :param device: device identifier, e.g. "TA9890AMTG".
    :param app: apk package name, e.g. "calc.apk".
    """
    downloads_path = os.path.expanduser('~') + "/Downloads/"
    template = "*.apk"
    newest_apk = max(glob.iglob(downloads_path + template), key=os.path.getctime)
    command = 'adb -s {0} install -r {1}{2}'.format(device, "" if get_sdk_version(device) < "17" else "-d ", newest_apk)
    log.info("Installing '{0}' onto device '{1}'...".format(newest_apk, device))
    console.execute(command)


def uninstall_app(device, package):
    """
    Uninstalls given application by its package name.

    :param device: device identifier, e.g. "TA9890AMTG".
    :param package: package name (e.g. com.android.calculator2).
    """
    command = "adb -s " + device + " uninstall " + package
    console.execute(command)


def start_app(device, package):
    """
    Launches application by the given package name and puts this to foreground.

    :param device: device identifier, e.g. "TA9890AMTG".
    :param package: package name (e.g. com.android.calculator2).
    """
    command = "adb -s " + device + " shell am start -n " + package
    console.execute(command)


def get_cpu_frequency(device):
    """
    Returns CPU frequency for the given device, GHz.

    :param device: Device to get its CPU frequency.
    :returns string: CPU frequency, e.g. "2.27".
    """
    command = 'adb -s {0} shell cat "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"'.format(device)
    stdout = console.execute(command)
    return "{0:.2f}".format(round(float(stdout) / 1000000, 2))


def get_ram_size(device):
    """
    Returns RAM size for the given device, GB.

    :param device: Device to get its RAM size.
    :returns string: RAM size, e.g. "1.90".
    """
    command = 'adb -s {0} shell cat /proc/meminfo'.format(device)
    stdout = console.execute(command)
    regex = "(?<=MemTotal:)\s+\d+(?= kB)"
    ram_size = re.findall(regex, stdout)[0].lstrip()
    return "{0:.2f}".format(round(float(ram_size) / 1000000, 2))


def get_resolution(device):
    """
    Returns display resolution for the given device.

    :param device: Device to get its resolution.
    :returns string: Device resolution, e.g. "1080x1920".
    """
    command1 = "adb -s {0} shell wm size".format(device)
    command2 = "adb -s {0} shell dumpsys window".format(device)
    regex = "\d{3,}x\d{3,}"
    stdout1 = console.execute(command1)
    stdout2 = console.execute(command2)
    matches1 = re.findall(regex, stdout1)
    matches2 = re.findall(regex, stdout2)
    return matches1[0].lstrip() if matches1 else matches2[0].lstrip() if matches2 else None


def get_android_version(device):
    """
    Returns Android OS version for the given device.

    :param device: Device to get its Android OS version.
    :returns string: Device Android version, e.g. "4.4.2".
    """
    command = "adb -s {0} shell getprop ro.build.version.release".format(device)
    return console.execute(command)


def get_device_model(device):
    """
    Returns device model for the given device.

    :param device: Device to get its model.
    :returns string: Device model name, e.g. "Nexus 5".
    """
    command = "adb -s {0} shell getprop ro.product.model".format(device)
    return console.execute(command)


def get_ip_address(device):
    """
    Returns network IP address used by the given device.

    :param device: Device to get its IP address.
    :returns string: IP address, e.g. "10.218.25.173".
    """
    command1 = "adb -s {0} shell ifconfig".format(device)
    command2 = "adb -s {0} shell netcfg".format(device)
    regex1 = "(?<=inet addr:)\d[^2]\d*\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    regex2 = "(?<=wlan0\s{4}UP)\s+[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    stdout1 = console.execute(command1)
    stdout2 = console.execute(command2)
    matches1 = re.findall(regex1, stdout1)
    matches2 = re.findall(regex2, stdout2)
    return matches1[0].lstrip() if matches1 else matches2[0].lstrip() if matches2 else None


def get_sdk_version(device):
    """
    Returns Android SDK version supported by the given device.

    :param device: Device to get its SDK version.
    :returns string: SDK version, e.g. "19".
    """
    command = "adb -s {0} shell getprop ro.build.version.sdk".format(device)
    return console.execute(command)


def get_language(device):
    """
    Returns current language set on the given device.

    :param device: Device to get its language.
    :returns string: Device language, e.g. "en".
    """
    command = "adb -s {0} shell getprop persist.sys.language".format(device)
    return console.execute(command)


def get_country(device):
    """
    Returns current country set on the given device.

    :param device: Device to get its country.
    :returns string: Device country, e.g. "US".
    """
    command = "adb -s {0} shell getprop persist.sys.country".format(device)
    return console.execute(command)


def get_manufacturer(device):
    """
    Returns manufacturer for the given device.

    :param device: Device to get its manufacturer.
    :returns string: device manufacturer, e.g. "motorola".
    """
    command = "adb -s {0} shell getprop ro.product.manufacturer".format(device)
    return console.execute(command)


def enter_text(device, text):
    """
    Enters given text on the device.

    :param device: string, Device identifier.
    :param text: string, Text to enter.
    """
    command = "adb -s {0} shell input text {1}".format(device, text)
    console.execute(command)


def switch_wifi(device, state):
    """
    Switches WiFi ON/OFF.

    :param device: string, Device identifier.
    :param state: ON to enable, OFF to disable.
    :returns string: Wifi state as number (0 - disabled, 1 - enabled).
    """
    current_wifi_state = _get_wifi_state(device)
    if (current_wifi_state == "0" and state == "OFF") or (current_wifi_state > "0" and state == "ON"):
        return log.warn("WiFi is already '{0}' on the device '{1}'".format(state, device))
    _open_wifi_settings(device)
    _send_key_event(device, "KEYCODE_DPAD_UP")
    _send_key_event(device, "KEYCODE_DPAD_UP")
    _send_key_event(device, "KEYCODE_DPAD_CENTER")
    _send_key_event(device, "KEYCODE_BACK")


def switch_cellular_data(device, state):
    """
    Switches cellular data ON/OFF.

    :param device: string, Device identifier.
    :param state: ON to enable, OFF to disable.
    """
    current_cellular_state = _get_cellular_data_state(device)
    if (current_cellular_state == "0" and state == "OFF") or (current_cellular_state > "0" and state == "ON"):
        return log.warn("Cellular Data is already '{0}' on the device '{1}'".format(state, device))
    _open_data_usage_settings(device)
    _send_key_event(device, "KEYCODE_DPAD_DOWN")
    # needed for certain Android 5.0 devices
    if state == "OFF":
        _send_key_event(device, "KEYCODE_DPAD_DOWN")
    _send_key_event(device, "KEYCODE_DPAD_CENTER")
    #  needed for certain Android 5.0 devices
    if state == "ON":
        _send_key_event(device, "KEYCODE_DPAD_DOWN")
        _send_key_event(device, "KEYCODE_DPAD_CENTER")
    # needed for confirmation dialog.
    if state == "OFF":
        _send_key_event(device, "KEYCODE_TAB")
    _send_key_event(device, "KEYCODE_ENTER")
    _send_key_event(device, "KEYCODE_BACK")


def _get_cellular_data_state(device):
    """
    Returns current WiFi state - enabled or not (0 - disabled, 1 - enabled).

    :param device: device identifier where to get Cellular Data state.
    :return string: Cellular Data state.
    """
    command = "adb -s {0} shell settings get global mobile_data".format(device)
    return console.execute(command)


def _open_data_usage_settings(device):
    """
    Opens Data Usage screen.

    :param device: string, device identifier.
    """
    command = 'adb -s {0} shell am start -n com.android.settings/.Settings\"\$\"DataUsageSummaryActivity'\
        .format(device)
    console.execute(command)


def _open_wifi_settings(device):
    """
    Opens WiFi settings screen.

    :param device: string, device identifier where to open WiFi settings.
    """
    command = "adb -s {0} shell am start -a android.intent.action.MAIN -n com.android.settings/.wifi.WifiSettings" \
        .format(device)
    console.execute(command)


def _get_wifi_state(device):
    """
    Returns current WiFi state - enabled or not (0 - disabled, 1 - enabled).

    :param device: device identifier where to get WiFi state.
    :return string: WiFi state.
    """
    command = "adb -s {0} shell settings get global wifi_on".format(device)
    return console.execute(command)


def _send_key_event(device, keycode):
    """
    Sends given key event onto the device.

    :param device: string, Device identifier to send key event to, e.g. "TA9890AMTG".
    :param keycode: string Key code to send, e.g. "KEYCODE_ENDCALL" or "6".
    """
    command = "adb -s {0} shell input keyevent {1}".format(device, keycode)
    console.execute(command)


def _grant_permissions_to_change_config(device, package):
    """
    Grants CHANGE_CONFIGURATION permissions for the given application specified by package.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param package: string, application package, e.g. "com.android.calculator2".
    """
    command = "adb -s " + device + " shell pm grant " + package + " android.permission.CHANGE_CONFIGURATION"
    console.execute(command)


def _is_app_installed(device, package):
    """
    Verifies if the given application is installed on the device.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param package: string, application package, e.g. "com.android.calculator2".
    :returns boolean: True if installed, otherwise False.
    """
    command = "adb -s {0} shell pm list packages".format(device)
    regex = "(?<=package:){0}[\r\n$]".format(package)
    stdout = console.execute(command)
    return True if re.findall(regex, stdout) else False


def _open_google_play_for_app(device, package):
    """
    Opens Google Play to install the given application.

    :param device: string, device identifier, e.g. "TA9890AMTG".
    :param package: string, application package, e.g. "com.android.calculator2".
    """
    command = "adb -s " + device + " shell am start -a android.intent.action.VIEW -d market://details?id=" + package
    console.execute(command)
