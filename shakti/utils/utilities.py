import ntpath
import subprocess
import re
import os
import shutil

from dotenv import load_dotenv, find_dotenv

from shakti.utils.constants import DATA_FILE_EXTS, MODEL_FILE_EXTS, INFRA_FILE_EXTS


def get_env_creds():
    try:
        os.chdir(os.getcwd())
        dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(dotenv_path=dotenv_path)
    except:
        raise AUTH_ERROR


def file_from_path(path):
    '''Get file name from path string'''
    # https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_filename_noext(filename):
    return file_from_path(
        filename).rsplit(".", maxsplit=1)[0]


def get_fileext(filename):
    return file_from_path(
        filename).rsplit(".", maxsplit=1)[1]


def run_bash_cmd(cmd):
    process = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return process.stdout


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


def cleanup_postdeploy():
    set_cwd()
    dir_contents = os.listdir(os.getcwd())
    for item in dir_contents:
        if any([item.endswith(ext) for ext in DATA_FILE_EXTS]) or any([item.endswith(ext) for ext in MODEL_FILE_EXTS]) or any([item.endswith(ext) for ext in INFRA_FILE_EXTS]):
            if os.path.isfile(item):
                os.remove(item)
            elif os.path.isdir(item):
                shutil.rmtree(item)
