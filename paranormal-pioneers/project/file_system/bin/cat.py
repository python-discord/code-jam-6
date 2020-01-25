from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class Cat(command.Command):
    """Print contents of a file.
    Example: cat .termrc
    """
    def __init__(self):
        super().__init__(name='cat')

    @command.option('path', nargs='?')
    def handle_path(self, ns: Namespace, term: Terminal) -> None:
        if ns.path is None:
            raise OSException('error: path not specified')
        self.path = term.fs.get_path(term.path, ns.path, check_dir=False)

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            if self.path.is_file():
                return self.path.read_text('utf-8')
            raise OSException('error: not a file')

        except OSError:
            raise OSException('error: no such file') from None


def setup(parser: Parser) -> None:
    parser.add_command(Cat())
