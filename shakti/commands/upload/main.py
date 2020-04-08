import os
from shakti.utils.gcp.googlebucket import gcs_file_upload
from shakti.utils.utilities import get_env_creds
from shakti.utils.constants import GCS_BUCKET_NAME


def upload(file_type, file_path, **kwargs):
    get_env_creds()
    bucket_name = kwargs.get(GCS_BUCKET_NAME, os.environ[GCS_BUCKET_NAME])
    gcs_file_upload(bucket_name, file_type, file_path)
