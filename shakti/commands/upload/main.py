from ...gcp_utils.googlebucket import gcs_bucket_upload


class Upload():
    def upload(self, **kwargs):
        file_path = kwargs.get("<filepath>", "")
        cloud = kwargs.get("cloud", "gcp")
        if cloud == "gcp":
            gcs_bucket_upload(file_path)
        else:
            print("Other clouds not currently supported")
