import fire
import os

from shakti.commands.upload.main import upload
from shakti.commands.list.main import list_files
from shakti.commands.deploy.main import deploy

from dotenv import load_dotenv, find_dotenv


def main():
    """Main CLI entrypoint."""
    fire.Fire({
        "upload": upload,
        "list": list_files,
        "deploy": deploy
    })
