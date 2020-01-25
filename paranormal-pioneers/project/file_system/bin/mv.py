from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class MV(command.Command):
    """Move or rename a file/directory."""
    def __init__(self) -> None:
        super().__init__(name='mv')

    @command.option('src', nargs='?')
    def handle_source(self, ns: Namespace, term: Terminal) -> None:
        if ns.src is None:
            raise OSException('error: source not given')

        self.src = term.fs.get_path(term.path, ns.src, check_dir=False)

    @command.option('dest', nargs='?')
    def handle_dest(self, ns: Namespace, term: Terminal) -> None:
        if ns.dest is None:
            raise OSException('error: destination not given')

        self.dest = term.fs.get_path(term.path, ns.dest, check_existing=False)

    def main(self, ns: Namespace, term: Terminal) -> None:
        if self.dest.is_dir():
            self.dest /= self.src.name

        self.src.rename(self.dest)


def setup(parser: Parser) -> None:
    parser.add_command(MV())
