from ...gcp_utils.googlebucket import gcs_bucket_upload


def upload(file_path, **kwargs):
    cloud = kwargs.get("cloud", "gcp")
    if cloud == "gcp":
        gcs_bucket_upload(file_path)
    else:
        print("Other clouds not currently supported")
