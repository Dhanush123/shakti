import os

from shakti.utils.utilities import run_bash_cmd
from shakti.utils.constants import PROJECT_ID, AUTH_ERROR


def gcp_auth():
    try:
        auth_list_cmd = "gcloud auth list"
        auth_output = run_bash_cmd(auth_list_cmd)
        if (auth_output and int(auth_output.find("No credentialed accounts.")) != -1):
            login_cmd = "gcloud auth login"
            run_bash_cmd(login_cmd)
    except:
        raise AUTH_ERROR


def gcp_setproject():
    try:
        list_cmd = "gcloud projects list"
        output = run_bash_cmd(list_cmd)
        project_id = os.environ[PROJECT_ID]
        if (output and int(output.find(project_id)) == -1) or error:
            config_cmd = "gcloud config set project {}".format(project_id)
            run_bash_cmd(config_cmd)
    except:
        raise AUTH_ERROR
