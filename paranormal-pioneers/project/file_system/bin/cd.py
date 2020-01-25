from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class CD(command.Command):
    """Change current directory.
    Example: cd bin
    """
    def __init__(self) -> None:
        super().__init__(name='cd')

    @command.option('dir', nargs='?', default='.')
    def set_dir(self, ns: Namespace, term: Terminal) -> None:
        self.path = term.fs.get_path(term.path, ns.dir)

    def main(self, ns: Namespace, term: Terminal) -> None:
        term._path = self.path


def setup(parser: Parser) -> None:
    parser.add_command(CD())
