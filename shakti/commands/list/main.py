from ...gcp_utils.googlebucket import gcs_list_files


class List():
    def list(self, **kwargs):
        list_type = kwargs.get("<listtype>", "")
        gcs_list_files(list_type)
