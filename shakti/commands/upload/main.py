from shakti.utils.gcp.googlebucket import gcs_file_upload


def upload(file_type, file_path):
    gcs_file_upload(file_type, file_path)
