from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class Copy(command.Command):
    """Move files or directories to another directory."""
    def __init__(self) -> None:
        super().__init__(name='cp')

    @command.option('paths', nargs='*')
    def handle_paths(self, ns: Namespace, term: Terminal) -> None:
        paths = ns.paths.copy()

        if len(paths) < 2:
            raise OSException('error: not enough paths given')

        *self.srcs, self.dest = (
            term.fs.get_path(term.path, path, check_dir=False)
            for path in paths
        )

    def main(self, ns: Namespace, term: Terminal) -> None:
        if not self.dest.is_dir():
            raise OSException('error: destination is not a directory')

        for src in self.srcs:
            try:
                src.copy(self.dest)
            except OSError:
                raise OSException('error: failed to copy path') from None


def setup(parser: Parser) -> None:
    parser.add_command(Copy())
