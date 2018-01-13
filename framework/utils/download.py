"""
This module contains a list of utilities related to downloading files, e.g. binary builds.
"""

import framework.utils.constants as constants
import framework.utils.console as console
import logging
import urllib2
import urllib
import os

log = logging.getLogger("mth.utils")


def download_file(url, out_relative_path):
    """
    Downloads file from the given URL.

    :param url: URL to download file.
    :param out_relative_path: string, Path where to save the downloaded file.
    """
    local_path = os.getcwd() + os.path.sep
    urllib.urlretrieve(url, local_path + out_relative_path)


def _download(download_url, save_path=constants.downloads_dir()):
    """
    Downloads file from given URL to specified folder.

    :param download_url: URL from where to download.
    :param save_path: Target file path where to save the downloaded file.
    """
    file_name = download_url.split('/')[-1]
    resource = urllib2.urlopen(download_url)
    downloaded_file = open(save_path + file_name, 'wb')
    meta = resource.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    read_status = 0
    block_size = 8192
    while True:
        read_buffer = resource.read(block_size)
        if not read_buffer:
            break
        downloaded_file.write(read_buffer)
        read_status += len(read_buffer)
        console.show_progress(read_status, file_size)
    downloaded_file.close()
    log.info("")
