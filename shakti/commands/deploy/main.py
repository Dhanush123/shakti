
from datetime import datetime

from shakti.utils.gcp.googlebucket import gcs_download_file
from shakti.utils.gcp.auth import gcp_auth, gcp_setproject
from shakti.utils.utilities import file_from_path, run_bash_cmd, filter_alpha, get_filename_noext
from shakti.utils.container import get_container_files, add_env_to_dockerfile, build_container, deploy_container, add_modelfilename_to_dockerfile
from shakti.utils.metadata import upload_model_metadata
from shakti.utils.constants import SKLEARN, TF


def deploy(model_path, model_type=SKLEARN, region="us-east1", auth="--allow-unauthenticated"):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        file_name = get_filename_noext(model_path)
        model_name = filter_alpha(file_name)
        date = str(datetime.now()).replace(
            ".", "-").replace(":", "-").replace(" ", "-")
        model_id = "{}-{}".format(model_name, date)

        local_model_path = gcs_download_file(model_path)

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
    except:
        raise Exception("Something went wrong in deploying the model.")
