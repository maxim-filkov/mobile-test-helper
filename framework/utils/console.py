"""
This module contains a list of utilities related to console.
"""

from __future__ import print_function
from select import select
import subprocess
import logging
import math
import sys
import os

log = logging.getLogger("mth.utils")


def execute(command, suppress_errors=False, out=subprocess.PIPE, io_mode="w+"):
    """
    Executes given command, redirect stdout to file or returns this as text if file path is not given. All suppressed
    stderr is redirected to debug log, so enable debugging level if needed.

    :param command: string or list, command to execute.
    :param suppress_errors: boolean, optional, set True if you don't want to see errors in output, by default False.
    :param out: string, optional, file path to redirect stdout to, by default stdout is returned as text.
    :param io_mode: input/output mode, e.g. (w)rite, (r)ead, (append)
    :returns: stdout as string (if the file path is not given).
    """
    command = command.split() if isinstance(command, str) else command
    process = None
    try:
        if out is subprocess.PIPE:
            process = subprocess.Popen(command, stdout=out, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if (stderr and suppress_errors) or stderr.startswith("WARNING"):
                log.debug(stderr)
            # adb returns code 0 and empty stderr for failed commands
            if process.returncode != 0 or "Failure" in stdout:
                message = "{0}{1}".format(stderr, stdout)
                log.error("Execution failed for '{0}' with the output:\n{1}".format(" ".join(command), message))
                sys.exit(1)
            return stdout.rstrip()
        else:
            directory = os.path.dirname(out)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(out, io_mode) as out:
                process = subprocess.Popen(command, stdout=out, stderr=subprocess.PIPE)
                process.wait()

    except KeyboardInterrupt:
        if process:
            process.kill()
            process.wait()


def prompt(input_prompt, timeout=None):
    """
    Prompts user to enter some info.

    :param input_prompt: string, input prompt text to show to user.
    :param timeout: max time to wait for user input, seconds.
    :returns string: info entered by user.
    """
    print(input_prompt, end='')
    sys.stdout.flush()
    inputs = [sys.stdin]
    if timeout:
        readable, writable, exceptional = select(inputs, [], [], timeout)
    else:
        readable, writable, exceptional = select(inputs, [], [])
    answer = ""
    if readable:
        answer = sys.stdin.readline()
    else:
        print("")
    return answer


def prompt_for_options(input_prompt, options, show_with_numbers=False):
    """
    Prompts user to enter some info. Be careful, this function accepts the entered options case insensitively.

    :param input_prompt: string, input prompt text to show to user.
    :param options: tuple of options to validate user input.
    :param show_with_numbers: for very long option strings, user can just use the index
    :returns string: info entered by user.
    """
    answer = ""
    low_options = [option.lower() for option in options]
    show_list_as_n_columns(options, 3, show_with_numbers)
    while answer.lower() not in low_options:
        answer = raw_input(input_prompt)
        if show_with_numbers is True:
            is_number = True
            for c in answer:
                if c.isdigit():
                    is_number = is_number and True
                else:
                    is_number = is_number and False

            if is_number is True and answer is not "" and int(answer) in xrange(len(low_options)):
                index = low_options.index(int(answer))
                return options[index]

    return answer


def show_list_as_n_columns(list_, n, show_with_numbers=False):
    """
    Prints the given list as several columns in console standard output.

    :param list_: list, a list to print out.
    :param n: int, how many columns to use.
    :param show_with_numbers: for very long option strings, user can just use the index
    """

    data_list = list(list_)

    if show_with_numbers is True:
        for i in xrange(len(data_list)):
            data_list[i] = "[{0}] ".format(i) + data_list[i]

    length = len(data_list)
    if length == 0:
        print("List is empty")
        return data_list

    if length == 1:
        print(data_list)
        return
    split_size = int(math.ceil(float(length)/float(n)))
    i = 0
    column_lists = []

    while i < n:
        column_lists.append(list(data_list[i * split_size:(i+1) * split_size]))
        i += 1

    while len(column_lists[0]) != len(column_lists[n - 1]):
        """ fill in any blank spaces in last column to avoid index errors """
        column_lists[n - 1].append(" ")

    for tup in zip(*column_lists):
        line = ""
        for num in xrange(n):
            line = line + "{0:<35s} \t ".format(tup[num])
        print(line)


def show_progress(step, size):
    """
    Shows progress bar in console.

    :param step: int, current step.
    :param size: int, maximum number of steps.
    """
    percentage = float(step / float(size)) * 100
    diff = 100 - percentage
    if step % 1 == 0:
        sys.stdout.write("\r[" + "#" * int(percentage) + " " * int(diff) + "]" + " {0:.2f}".format(percentage) + "%")
        sys.stdout.flush()


def compress_video(video_file_path):
    """
    Compresses the given video file.

    :param video_file_path: path to video file to compress.
    """
    """
    :param video_file_path:
    :return:
    """
    log.info("Compression video...")
    command = ["ffmpeg", "-i", video_file_path, "-vcodec", "libx264", "-crf", "20", video_file_path + ".out.mp4"]
    execute(command, True)
    os.rename(video_file_path + ".out.mp4", video_file_path)


def touch(file_name):
    """
    Touches a file - changes its date to the newest.

    :param file_name: File name to touch.
    """
    if os.path.exists(file_name):
        os.utime(file_name, None)
    else:
        open(file_name, 'a').close()
