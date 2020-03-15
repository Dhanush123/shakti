import ntpath
import subprocess
import re
import os


def file_from_path(path):
    '''Get file name from path string'''
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_filename_noext(filename):
    return file_from_path(
        filename).rsplit(".", maxsplit=1)[0]


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


def replace_tuples_with_lists(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, tuple):
            dictionary[key] = list(value)
        elif isinstance(value, dict):
            dictionary[key] = replace_tuples_with_lists(dictionary)
    return dictionary
