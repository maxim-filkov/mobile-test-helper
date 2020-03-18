"""
This module contains a list of constants.
"""

import os


def arm_architectures():
    """
    :returns tuple: all available Android architectures.
    """
    return "armv7", "arm64"


def locales():
    """
    Returns a tuple of supported locales.

    :returns locales: a tuple of all supported locales.
    """
    return ("en-US", "es-ES", "fr-FR", "pt-BR", "de-DE", "it-IT", "ru-RU", "tr-TR",
            "th-TH", "vi-VN", "zh-TW", "zh-CN", "ja-JP", "ko-KR", "iw-IL", "ar-EG",
            "ms-MY", "in-ID", "pl-PL", "tl-PH", "ur-IN", "hi-IN", "my-US", "bn-BD")


def platforms():
    """
    Returns a tuple of supported platforms.

    :returns apps: a tuple of all supported platforms.
    """
    return "android", "ios"


def log_levels():
    """
    :returns list: list of all supported logging levels.
    """
    return ["error", "warn", "info", "debug", "trace"]


def downloads_dir():
    """
    :returns string: default downloads directory path.
    """
    return os.path.expanduser('~') + "/Downloads/"
