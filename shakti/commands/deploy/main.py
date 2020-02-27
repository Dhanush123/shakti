import os
import shutil
import subprocess

from shaktiutils.gcp_utils.googlebucket import gcs_download_file
from shaktiutils.gcp_utils.auth import gcp_auth, gcp_setproject
from shaktiutils.constants import PROJECT_ID
from shaktiutils.utilities import file_from_path, run_bash_cmd
import shakti.deploy_templates.docker.flask


def deploy(model_path, model_type="flask", region="us-east1", auth="--allow-unauthenticated"):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        model_name = file_from_path(
            model_path).rsplit(".", maxsplit=1)[0]

        gcs_download_file(model_path)
        get_docker_files(model_type)
        gcp_auth()
        gcp_setproject()
        build_container(model_name)
        deploy_container(model_name, region, auth)
    except:
        raise Exception


def get_docker_files(model_type):
    data_dir = os.path.join(os.path.dirname(__file__),
                            "commands", "deploy_templates", "docker", model_type)
    dockerfile_name = "Dockerfile"
    dockerignore_name = ".dockerignore"
    dockerfile_path = os.path.join(data_dir, dockerfile_name)
    dockerignore_path = os.path.join(data_dir, dockerignore_name)
    shutil.move(os.path.join(dockerfile_path, dockerfile_name), os.getcwd())
    shutil.move(os.path.join(dockerignore_path,
                             dockerignore_name), os.getcwd())


def build_container(model_name):
    # https://stackoverflow.com/questions/48066114/execute-bash-commands-python-way
    # https://stackoverflow.com/questions/52415779/python-run-bash-commands-sequentially
    # https://cloud.google.com/run/docs/quickstarts/build-and-deploy
    # TODO: revist this if output & error don't print out
    # running bash cmd in python here, need to do this b/c there isn't a python sdk for this yet
    try:
        imagebuild_cmd = "gcloud builds submit --tag gcr.io/{}/{}".format(
            os.environ([PROJECT_ID]), model_name)
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

    # TODO: if not use cloudbuild.yaml for CD from GitHub, remove this function & the yaml file
    # def get_build_files():
    #     data_dir = os.path.join(os.path.dirname(__file__),
    #                             "commands", "deploy_templates", "docker", "other")
    #     cloudbuild_name = "cloudbuild.yaml"
    #     cloudbuild_path = os.path.join(data_dir, cloudbuild_name)
    #     cloudbuild_data = None
    #     with open(cloudbuild_path, 'r') as file:
    #         cloudbuild_data = file.read()

    #     # Replace the target string
    #     cloudbuild_data = cloudbuild_data.replace('ram', 'abcd')

    #     # Write the file out again
    #     with open('file.txt', 'w') as file:
    #         file.write(filedata)
