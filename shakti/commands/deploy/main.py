import os

from shakti.utils.gcp.googlebucket import gcs_download_file
from shakti.utils.gcp.auth import gcp_auth, gcp_setproject
from shakti.utils.utilities import get_env_creds, file_from_path, run_bash_cmd, filter_alpha, get_filename_noext, cleanup_postdeploy, get_date_for_id
from shakti.utils.container import get_container_files, add_env_to_dockerfile, build_container, deploy_container, add_modelfilename_to_dockerfile
from shakti.utils.metadata import upload_model_metadata
from shakti.commands.upload.main import upload
from shakti.utils.constants import SKLEARN, TF, GCP_REGION, CLOUD_RUN_AUTH, CLOUD_RUN_DEFAULT_AUTH, GCP_DEFAULT_REGION, CLOUD, LOCAL, MODELS, DEPLOY_ERROR


def deploy(model_type, model_location, model_path, **kwargs):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        get_env_creds()
        file_name = get_filename_noext(model_path)
        model_name = filter_alpha(file_name)
        date = get_date_for_id()
        model_id = "{}-{}".format(model_name, date)

        region = kwargs.get(GCP_REGION, os.environ.get(
            GCP_REGION, GCP_DEFAULT_REGION))
        auth = kwargs.get(CLOUD_RUN_AUTH, os.environ.get(
            CLOUD_RUN_AUTH, CLOUD_RUN_DEFAULT_AUTH))

        local_model_path = gcs_download_file(
            model_path) if model_location == CLOUD else model_path

        if model_location == LOCAL:
            upload(MODELS, local_model_path)

        if model_type == SKLEARN:
            get_container_files(model_type)
            add_env_to_dockerfile()
            gcp_auth()
            gcp_setproject()
            upload_model_metadata(local_model_path, model_id, model_type)
            build_container(model_id)
            deploy_container(model_id, region, auth)
        elif model_type == TF:
            get_container_files(model_type)
            # adding .pb to ensure .pb file is always picked
            add_modelfilename_to_dockerfile(
                file_name+".pb", model_type)
            gcp_auth()
            gcp_setproject()
            upload_model_metadata(local_model_path, model_id, model_type)
            # cloud build yaml file has build + deploy
            build_container(model_id)
            deploy_container(model_id, region, auth)
        cleanup_postdeploy()
    except:
        raise Exception(DEPLOY_ERROR)
