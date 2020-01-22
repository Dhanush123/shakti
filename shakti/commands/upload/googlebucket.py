from google.cloud import storage
import os
import sys

from ...testing import GCS_BUCKET_NAME
from ...utilities import name_from_path


def gcs_bucket_upload(file_path):
    """Uploads a file to the bucket."""
    # file_path = "local/path/to/file"
    # GCS_BUCKET_NAME = "bucketname"
    # https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python

    storage_client = storage.Client()

    bucket = storage_client.bucket(os.environ[GCS_BUCKET_NAME])
    print("uploading", file_path)
    # print("ALL ENV!!!!", os.environ)
    try:
        # source and destination file name are kept same
        file_name = name_from_path(file_path)
        blob = bucket.blob("models/"+file_name)
        blob.upload_from_filename(file_path)
        print("File {} has been uploaded".format(file_name))
    except KeyError:
        print("Please set the environment variable {}".format(GCS_BUCKET_NAME))
