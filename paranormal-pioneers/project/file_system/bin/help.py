from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Help(command.Command):
    def __init__(self) -> None:
        super().__init__(name='help')

    def main(self, ns: Namespace, term: Terminal) -> None:
        message = ('\n\n').join(
            command.format_help() for command in term.parser.list_commands()
        )
        return message


def setup(parser: Parser) -> None:
    parser.add_command(Help())
