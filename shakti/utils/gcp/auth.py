import os

from shakti.utils.utilities import run_bash_cmd
from shakti.utils.constants import PROJECT_ID
from dotenv import load_dotenv, find_dotenv


def gcp_auth():
    try:
        auth_list_cmd = "gcloud auth list"
        auth_output, auth_error = run_bash_cmd(auth_list_cmd)
        auth_output = auth_output.decode(
            "utf-8") if auth_output else auth_output
        auth_error = auth_error.decode(
            "utf-8") if auth_error else auth_error
        print("ao", auth_output)
        print("ae", auth_error)
        if (auth_output and auth_output.find("No credentialed accounts.") != -1):
            login_cmd = "gcloud auth login"
            login_output, login_error = run_bash_cmd(login_cmd)
    except:
        raise


def gcp_setproject():
    list_cmd = "gcloud projects list"
    output, error = run_bash_cmd(list_cmd)
    output = output.decode(
        "utf-8") if output else output
    error = error.decode(
        "utf-8") if error else error
    project_id = os.environ[PROJECT_ID]
    if (output and int(output.find(project_id)) == -1) or error:
        config_cmd = "gcloud config set project {}".format(project_id)
        run_bash_cmd(config_cmd)


def get_env_creds():
    os.chdir(os.getcwd())
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path=dotenv_path)
