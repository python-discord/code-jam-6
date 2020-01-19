from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import IOTerminal


class CD(command.Command):
    def __init__(self) -> None:
        super().__init__(name='cd')

    @command.option('dir', nargs='?', default='.')
    def set_dir(self, ns: Namespace, term: IOTerminal) -> None:
        self.path = term.api.change_dir(term.path, ns.dir)

    def main(self, ns: Namespace, term: IOTerminal) -> None:
        term._path = self.path


def setup(parser: Parser) -> None:
    parser.add_command(CD())
