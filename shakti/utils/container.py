import os
import shutil
import subprocess
from dotenv.main import dotenv_values
from pathlib import Path

from shakti.utils.constants import PROJECT_ID, DOCKER_ENV_VARS_PLACEMENT, DOCKERFILE, DOCKERIGNORE, MODEL_ROUTE
from shakti.utils.utilities import run_bash_cmd


def get_container_files(server_type):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "deploytemplates", "docker", server_type))
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
