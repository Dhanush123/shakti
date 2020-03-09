from shakti.utils.gcp.googlebucket import gcs_file_upload


def upload(file_path, file_type="models"):
    gcs_file_upload(file_path, file_type)
