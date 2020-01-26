from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class RMDir(command.Command):
    """Remove an empty directory."""
    def __init__(self) -> None:
        super().__init__(name='rmdir')

    @command.option('dir', nargs='?')
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        if ns.dir is None:
            raise OSException('error: dir not specified')

        self.dir = term.fs.get_path(term.path, ns.dir)

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            self.dir.rmdir()
        except OSError:
            raise OSException('error: directory not empty') from None


def setup(parser: Parser) -> None:
    parser.add_command(RMDir())
