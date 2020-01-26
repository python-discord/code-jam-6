from argparse import Namespace
from datetime import datetime

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Date(command.Command):
    """Print current time.
    Example: date
    """
    def __init__(self) -> None:
        super().__init__(name='date')

    def main(self, ns: Namespace, term: Terminal) -> str:
        return datetime.now().strftime('%a %b %d %H:%M:%S %Y')


def setup(parser: Parser) -> None:
    parser.add_command(Date())
