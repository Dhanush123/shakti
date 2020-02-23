# """
# shakti

# Usage:
#   shakti upload <filepath>
#   shakti list <listtype>

# Examples:
#   shakti upload ~/Downloads/mnist_model.pkl
#   shakti list models

# Help:
#   For help using this tool, please open an issue on the Github repository:
#   https://github.com/Dhanush123/shakti
# """

# from inspect import getmembers, isclass
# from docopt import docopt
import fire
from dotenv import load_dotenv
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
