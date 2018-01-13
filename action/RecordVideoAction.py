"""
This module contains actions related to recording video from connected mobile device.
"""

import framework.utils.argparsing.completion as completion
import framework.utils.argparsing.defaults as defaults
import framework.utils.argparsing.types as types
from action.ActionFactory import ActionFactory
import framework.utils.android as android
import framework.utils.console as console
import logging
import os

log = logging.getLogger("action")


class RecordVideoAction(object):
    """
    Action for recording video.
    """

    __metaclass__ = ActionFactory

    class Meta(object):
        """
        Meta class to describe action.
        """
        action = "video"
        help = "Record video from device"

    @staticmethod
    def init_parser(parser):
        """
        Initializes argument parser with own arguments.

        :param parser: argparse.ArgumentParser, parser instance to initialize it with custom arguments.
        """
        parser.add_argument("--device", "-d",
                            help="Device to record video from",
                            type=types.connected_android_device,
                            default=defaults.connected_android_device()).completer = completion.android_devices
        parser.add_argument("--bitrate", "-b",
                            help="Video bit rate, by default 8000000 (6Mbps)",
                            type=int,
                            default=8000000)
        parser.add_argument("--timeout", "-t",
                            help="Maximum video duration, seconds (shouldn't exceed 180)",
                            type=types.adb_video_limit,
                            default=180)
        parser.add_argument("--compress", "-c",
                            help="Compress video after recording or not, by default True",
                            type=bool,
                            default=True).completer = completion.truefalse

    def __call__(self, device, timeout, bitrate, compress):
        """
        Takes one or more screenshots from specified device.

        :param device: string, device identifier, e.g. "TA9890AMTG".
        :param timeout: int, maximum duration for video, seconds.
        :param bitrate: int, video bit-rate, megabits per second.
        :param compress: boolean, compress out video or not, by default yes.
        """
        if device is None:
            devices = android.list_devices()
            device = console.prompt_for_options("Choose device: ", devices)
        current_dir = os.getcwd()
        file_path_on_device = android.record_video(device, timeout, bitrate)
        file_name = os.path.basename(file_path_on_device)
        android.download_file(device, file_path_on_device, current_dir)
        android.remove_file(device, file_path_on_device)
        result_file_path = os.path.join(current_dir, file_name)
        if compress:
            console.compress_video(result_file_path)
        log.info("Find result at " + result_file_path)
