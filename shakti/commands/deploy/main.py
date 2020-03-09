import os
import shutil
import subprocess
from dotenv.main import dotenv_values
from pathlib import Path
from datetime import datetime

from shakti.utils.gcp.googlebucket import gcs_download_file
from shakti.utils.gcp.auth import gcp_auth, gcp_setproject
from shakti.utils.constants import PROJECT_ID, DOCKER_ENV_VARS_PLACEMENT, DOCKERFILE, DOCKERIGNORE, MODEL_ROUTE
from shakti.utils.utilities import file_from_path, run_bash_cmd, filter_alpha


def deploy(model_path, model_type="flask", region="us-east1", auth="--allow-unauthenticated"):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        model_name = filter_alpha(file_from_path(
            model_path).rsplit(".", maxsplit=1)[0])
        date = str(datetime.now()).replace(
            ".", "-").replace(":", "-").replace(" ", "-")

        gcs_download_file(model_path)
        get_container_files(model_type)
        add_env_to_dockerfile()
        gcp_auth()
        gcp_setproject()
        model_id = "{}-{}".format(model_name, date)
        build_container(model_id)
        deploy_container(model_id, region, auth)
    except:
        raise Exception("Something went wrong in deploying the model.")


def get_container_files(model_type):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "..", "deploytemplates", "docker", model_type))
    dockerfile_path = os.path.join(data_dir, DOCKERFILE)
    dockerignore_path = os.path.join(data_dir, DOCKERIGNORE)
    # files will be overwritten if exist
    shutil.copy(dockerfile_path,  os.path.join(os.getcwd(), DOCKERFILE))
    shutil.copy(dockerignore_path,  os.path.join(
        os.getcwd(), DOCKERIGNORE))


def add_env_to_dockerfile():
    env_path = Path(os.path.join(os.getcwd(), ".env"))
    env_vars = dotenv_values(env_path)
    dockerfile_path = os.path.join(os.getcwd(), DOCKERFILE)

    with open(dockerfile_path, "r") as original_file:
        buf = original_file.readlines()

    with open(dockerfile_path, "w") as modified_file:
        for line in buf:
            if line == DOCKER_ENV_VARS_PLACEMENT:
                for key, value in env_vars.items():
                    line += "ENV {} {}\n".format(key, value)
            modified_file.write(line)


def build_container(model_id):
    # https://stackoverflow.com/questions/48066114/execute-bash-commands-python-way
    # https://stackoverflow.com/questions/52415779/python-run-bash-commands-sequentially
    # https://cloud.google.com/run/docs/quickstarts/build-and-deploy
    # TODO: revist this if output & error don't print out
    # running bash cmd in python here, need to do this b/c there isn't a python sdk for this yet
    try:
        imagebuild_cmd = "gcloud builds submit --tag gcr.io/{}/{}".format(
            os.environ[PROJECT_ID], model_id)
        output, error = run_bash_cmd(imagebuild_cmd)
    except:
        raise Exception("Something went wrong in building the container.")


def deploy_container(model_id, region, auth):
    try:
        deploy_cmd = "gcloud run deploy {} --image gcr.io/{}/{} --platform managed --region {} {}".format(
            model_id, os.environ[PROJECT_ID], model_id, region, auth)
        run_bash_cmd(deploy_cmd)
        print(
            "Make predictions by appending /{} to the deployment url above.".format(
                os.getenv(MODEL_ROUTE, "")))
    except:
        raise Exception("Something went wrong in deploying the container.")
