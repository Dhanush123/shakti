from shakti.commands.upload.googlebucket import gcs_bucket_upload
from json import dumps

from ..basecmd import BaseCmd


class Upload(BaseCmd):
    def upload(self, **kwargs):
        print("You supplied the following options:",
              dumps(kwargs, indent=2, sort_keys=True))
        file_path = kwargs.get("<filepath>", "")
        cloud = kwargs.get("cloud", "gcp")
        if cloud == "gcp":
            gcs_bucket_upload(file_path)
        else:
            print("Other clouds not currently supported")
