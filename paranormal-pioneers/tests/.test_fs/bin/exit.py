from argparse import Namespace
from os import _exit
from typing import NoReturn

from project.core import command
from project.core.log import log
from project.core.parser import Parser
from project.core.terminal import IOTerminal


class Exit(command.Command):
    def __init__(self):
        super().__init__(name='exit')

    @command.option('code', nargs='?', type=int, default=0)
    def handle_code(self, ns: Namespace, term: IOTerminal) -> None:
        self.code = ns.code

    def main(self, ns: Namespace, term: IOTerminal) -> NoReturn:
        log.critical(f'exit: {self.code}')
        _exit(self.code)


def setup(parser: Parser) -> None:
    parser.add_command(Exit())
