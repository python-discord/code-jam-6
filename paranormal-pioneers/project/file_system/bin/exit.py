from argparse import Namespace
from os import _exit
from typing import NoReturn

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Exit(command.Command):
    """Exit terminal with given code.
    Example: exit -1
    """
    def __init__(self) -> None:
        super().__init__(name='exit')

    @command.option('code', nargs='?', type=int, default=0)
    def handle_code(self, ns: Namespace, term: Terminal) -> None:
        self.code = ns.code

    def main(self, ns: Namespace, term: Terminal) -> NoReturn:
        _exit(self.code)


def setup(parser: Parser) -> None:
    parser.add_command(Exit())
