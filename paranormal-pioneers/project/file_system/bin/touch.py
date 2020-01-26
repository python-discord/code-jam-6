from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class Touch(command.Command):
    """Create (touch) a new file."""
    def __init__(self) -> None:
        super().__init__(name='touch')

    @command.option('path', nargs='?')
    def handle_path(self, ns: Namespace, term: Terminal) -> None:
        if ns.path is None:
            raise OSException('error: path not specified')

        self.path = term.fs.get_path(term.path, ns.path, check_existing=False)

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            self.path.touch()
        except OSError:
            raise OSException('error: no such file or directory') from None


def setup(parser: Parser) -> None:
    parser.add_command(Touch())
