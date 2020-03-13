
from datetime import datetime

from shakti.utils.gcp.googlebucket import gcs_download_file
from shakti.utils.gcp.auth import gcp_auth, gcp_setproject
from shakti.utils.utilities import file_from_path, run_bash_cmd, filter_alpha
from shakti.utils.container import get_container_files, add_env_to_dockerfile, build_container, deploy_container
from shakti.utils.metadata import upload_model_metadata
from shakti.utils.constants import SKLEARN


def deploy(model_path, model_type=SKLEARN, region="us-east1", auth="--allow-unauthenticated"):
    '''
    model_path is path inside cloud bucket, not local path
    '''
    try:
        model_name = filter_alpha(file_from_path(
            model_path).rsplit(".", maxsplit=1)[0])
        date = str(datetime.now()).replace(
            ".", "-").replace(":", "-").replace(" ", "-")

        local_model_path = gcs_download_file(model_path)
        get_container_files(model_type)
        add_env_to_dockerfile()
        gcp_auth()
        gcp_setproject()
        model_id = "{}-{}".format(model_name, date)
        upload_model_metadata(local_model_path, model_id, model_type)
        build_container(model_id)
        deploy_container(model_id, region, auth)
    except:
        raise Exception("Something went wrong in deploying the model.")
