from ...gcp_utils.googlebucket import gcs_list_files


def list_files(list_type, **kwargs):
    cloud = kwargs.get("cloud", "gcp")
    if cloud == "gcp":
        gcs_list_files(list_type)
    else:
        print("Other clouds not currently supported")
