from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class PWD(command.Command):
    """Print current working directory."""
    def __init__(self) -> None:
        super().__init__(name='pwd')

    def main(self, ns: Namespace, term: Terminal) -> str:
        return str(term.path)


def setup(parser: Parser) -> None:
    parser.add_command(PWD())
