from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class MKDir(command.Command):
    """Create a new directory.
    Example: mkdir test
    """
    def __init__(self) -> None:
        super().__init__(name='mkdir')

    @command.option('-r', '--resolve', action='store_true', default=False)
    def handle_resolving(self, ns: Namespace, term: Terminal) -> None:
        self.resolve = ns.resolve

    @command.option('dir', nargs='?')
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        if ns.dir is None:
            raise OSException('error: path not specified')

        self.dir = term.fs.get_path(term.path, ns.dir, check_existing=False)

    def main(self, ns: Namespace, term: Terminal) -> None:
        if self.dir.exists():
            raise OSException('error: path already exists')
        try:
            if self.resolve:
                path, parts = self.dir.clone(), list()

                while not path.exists():
                    parts.append(path.name)
                    path = path.parent

                for part in reversed(parts):
                    path /= part
                    path.mkdir()

            else:
                self.dir.mkdir()

        except OSError:
            raise OSException('error: can not find path') from None


def setup(parser: Parser) -> None:
    parser.add_command(MKDir())
