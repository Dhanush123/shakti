import os
import shutil
import subprocess
from dotenv.main import dotenv_values
from pathlib import Path

from shakti.utils.constants import PROJECT_ID, DOCKER_ENV_VARS_PLACEMENT, DOCKERFILE, DOCKERIGNORE, MODEL_ROUTE, CONTAINER_ERROR, TF, CLOUDBUILD, TF_SERVING_FOLDER
from shakti.utils.utilities import run_bash_cmd


def get_container_files(model_type):
    docker_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              "..", "deploytemplates", "docker", model_type))
    dockerfile_path = os.path.join(docker_dir, DOCKERFILE)
    dockerignore_path = os.path.join(docker_dir, DOCKERIGNORE)

    # files will be overwritten if exist
    shutil.copy(dockerfile_path, os.path.join(os.getcwd(), DOCKERFILE))

    if os.path.exists(dockerignore_path):
        shutil.copy(dockerignore_path, os.path.join(os.getcwd(), DOCKERIGNORE))

    # if model_type == TF:
    #     buildconfig_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
    #                                                    "..", "deploytemplates", "buildconfig", TF))
    #     tf_yaml_path = os.path.join(buildconfig_dir, CLOUDBUILD)
    #     shutil.copy(tf_yaml_path, os.path.join(os.getcwd(), CLOUDBUILD))


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


def build_container(model_id, yaml=False):
    # https://stackoverflow.com/questions/48066114/execute-bash-commands-python-way
    # https://stackoverflow.com/questions/52415779/python-run-bash-commands-sequentially
    # https://cloud.google.com/run/docs/quickstarts/build-and-deploy
    # running bash cmd in python here, need to do this b/c there isn't a python sdk for this yet
    try:
        imagebuild_cmd = "gcloud builds submit --tag gcr.io/{}/{}".format(
            os.environ[PROJECT_ID], model_id)
        run_bash_cmd(imagebuild_cmd)
    except:
        raise Exception(CONTAINER_ERROR)


def deploy_container(model_id, region, auth):
    try:
        deploy_cmd = "gcloud run deploy {} --image gcr.io/{}/{} --platform managed --region {} {}".format(
            model_id, os.environ[PROJECT_ID], model_id, region, auth)
        run_bash_cmd(deploy_cmd)
        print(
            "Make predictions by appending /{} to the deployment url above.".format(
                os.getenv(MODEL_ROUTE, "")))
    except:
        raise Exception(CONTAINER_ERROR)


def add_modelfilename_to_dockerfile(file_name, model_type):
    dockerfile_path = os.path.join(os.getcwd(), DOCKERFILE)

    with open(dockerfile_path, "r") as original_file:
        buf = original_file.readlines()

    with open(dockerfile_path, "w") as modified_file:
        for line in buf:
            if line.find("TF_SERVING_FOLDER"):
                line = line.replace("TF_SERVING_FOLDER", TF_SERVING_FOLDER)
            modified_file.write(line)
