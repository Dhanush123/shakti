"""
shakti
 
Usage:
  shakti upload <filepath>
  shakti list <listtype>

Examples:
  shakti upload ~/Downloads/mnist_model.pkl 
  shakti list models
 
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/Dhanush123/shakti
"""

from inspect import getmembers, isclass
from docopt import docopt
from dotenv import load_dotenv
import os

from shakti.commands.upload.main import Upload
from shakti.commands.list.main import List

CMDS = {"upload": Upload, "list": List}


def main():
    """Main CLI entrypoint."""
    load_dotenv()
    options = docopt(__doc__)
    print(options)
    for cmd, value in options.items():
        if value and cmd in CMDS:
            getattr(CMDS[cmd](), cmd)(**options)
            break
        # if hasattr(shakti.commands, k):
        #     module = getattr(shakti.commands, k)
        #     shakti.commands = getmembers(module, isclass)
        #     command = [command[1]
        #                for command in shakti.commands if command[0] != 'Base'][0]
        #     command = command(options)
        #     command.run()
