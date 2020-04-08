import os

from shakti.utils.gcp.googlebucket import gcs_list_files
from shakti.utils.utilities import get_env_creds
from shakti.utils.constants import GCS_BUCKET_NAME


def list_files(list_type, **kwargs):
    get_env_creds()
    bucket_name = kwargs.get(GCS_BUCKET_NAME, os.environ[GCS_BUCKET_NAME])
    gcs_list_files(bucket_name, list_type)
