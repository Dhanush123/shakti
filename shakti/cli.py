import fire
import os

from shakti.commands.upload.main import upload
from shakti.commands.list.main import list_files


def main():
    """Main CLI entrypoint."""
    load_dotenv()
    fire.Fire({
        "upload": upload,
        "list": list_files
    })
