from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.path import Path
from project.core.terminal import Terminal
from project.core.utils import OSException


class RM(command.Command):
    """Remove given file or directory."""
    def __init__(self) -> None:
        super().__init__(name='rm')

    @command.option('-d', '--dir', action='store_true', default=False)
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        self.dir = ns.dir

    @command.option('-r', '--recursive', action='store_true', default=False)
    def handle_recursive(self, ns: Namespace, term: Terminal) -> None:
        self.recursive = ns.recursive

    @command.option('path', nargs='?')
    def handle_file(self, ns: Namespace, term: Terminal) -> None:
        if ns.path is None:
            raise OSException('error: path is not specified')

        self.path = term.fs.get_path(term.path, ns.path, check_dir=False)

    def main(self, ns: Namespace, term: Terminal) -> None:
        is_dir = self.path.is_dir()

        try:
            if self.recursive:
                delete_recursive(self.path)
            elif is_dir:
                if self.dir:
                    self.path.rmdir()
                else:
                    raise OSException('error: is a directory')
            else:
                if self.dir:
                    raise OSException('error: not a directory')
                else:
                    self.path.unlink()

        except OSError:
            raise OSException('error: failed to remove given path') from None


def delete_recursive(path: Path) -> None:
    for inner in path.iterdir():
        if inner.is_dir():
            delete_recursive(inner)
        else:
            inner.unlink()
    path.rmdir()


def setup(parser: Parser) -> None:
    parser.add_command(RM())
