import ntpath
import subprocess
import re
import os


def file_from_path(path):
    '''Get file name from path string'''
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def run_bash_cmd(cmd):
    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE)
    # process.wait()
    output, error = process.communicate()
    return output, error


def filter_alpha(string):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', string)


def set_cwd():
    os.chdir(os.getcwd())
