import os
import shutil
import subprocess
from dotenv.main import dotenv_values
from pathlib import Path

from shaktiutils.gcp_utils.googlebucket import gcs_download_file
from shaktiutils.gcp_utils.auth import gcp_auth
from shaktiutils.gcp_utils.project import gcp_setproject
from shaktiutils.constants import PROJECT_ID, DOCKER_ENV_VARS_PLACEMENT, DOCKERFILE, DOCKERIGNORE
from shaktiutils.utilities import file_from_path, run_bash_cmd, filter_alpha


def deploy(model_path, model_type="flask", region="us-east1", auth="--allow-unauthenticated"):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        model_name = file_from_path(
            model_path).rsplit(".", maxsplit=1)[0]

        gcs_download_file(model_path)
        get_container_files(model_type)
        # add_data_to_dockerfile(model_name=model_name)
        add_env_to_dockerfile()
        gcp_auth()
        gcp_setproject()
        model_name = filter_alpha(model_name)
        build_container(model_name)
        deploy_container(model_name, region, auth)
    except:
        raise Exception


def get_container_files(model_type):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "..", "deploy_templates", "docker", model_type))
    dockerfile_path = os.path.join(data_dir, DOCKERFILE)
    dockerignore_path = os.path.join(data_dir, DOCKERIGNORE)
    # files will be overwritten if exist
    shutil.copy(dockerfile_path,  os.path.join(os.getcwd(), DOCKERFILE))
    shutil.copy(dockerignore_path,  os.path.join(
        os.getcwd(), DOCKERIGNORE))


# def add_data_to_dockerfile(**kwargs):
#     add_env()
#     add_model_name(kwargs.get("model_name"))

# def add_model_name(model_name):
#     dockerfile_path = os.path.join(os.getcwd(), DOCKERFILE)

#     with open(dockerfile_path, "r") as original_file:
#         buf = original_file.readlines()

#     with open(dockerfile_path, "w") as modified_file:
#         for line in buf:
#             if line == DOCKER_ENV_VARS_PLACEMENT:
#                 for key, value in env_vars.items():
#                     line += "ENV {} {}\n".format(key, value)
#             modified_file.write(line)


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


def build_container(model_name):
    # https://stackoverflow.com/questions/48066114/execute-bash-commands-python-way
    # https://stackoverflow.com/questions/52415779/python-run-bash-commands-sequentially
    # https://cloud.google.com/run/docs/quickstarts/build-and-deploy
    # TODO: revist this if output & error don't print out
    # running bash cmd in python here, need to do this b/c there isn't a python sdk for this yet
    try:
        imagebuild_cmd = "gcloud builds submit --tag gcr.io/{}/{}".format(
            os.environ[PROJECT_ID], model_name)
        output, error = run_bash_cmd(imagebuild_cmd)
    except:
        raise


def deploy_container(model_name, region, auth):
    try:
        deploy_cmd = "gcloud run deploy {} --image gcr.io/{}/{} --platform managed --region {} {}".format(
            model_name, os.environ[PROJECT_ID], model_name, region, auth)
        run_bash_cmd(deploy_cmd)
    except:
        raise
