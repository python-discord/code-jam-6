from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class Copy(command.Command):
    """Move a file or a directory to another directory."""
    def __init__(self) -> None:
        super().__init__(name='cp')

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
        if not self.dest.is_dir():
            raise OSException('error: destination is not a directory')
        try:
            self.src.copy(self.dest)
        except OSError:
            raise OSException('error: failed to copy path') from None


def setup(parser: Parser) -> None:
    parser.add_command(Copy())
