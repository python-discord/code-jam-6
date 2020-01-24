from argparse import Namespace
from datetime import datetime
from dateutil import tz

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Date(command.Command):
    """Display the current date and time."""

    def __init__(self) -> None:
        super().__init__(name='date')

    def main(self, ns: Namespace, term: Terminal) -> str:
        return datetime.now(tz.tzlocal()).strftime('%a %b %d %H:%M:%S %z %Y')


def setup(parser: Parser) -> None:
    parser.add_command(Date())
