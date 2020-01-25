from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Help(command.Command):
    """Print help about specified commands,
    or all commands, if none given.
    Example: help ls.
    """
    def __init__(self) -> None:
        super().__init__(name='help')

    @command.option('command', nargs='*')
    def handle_commands(self, ns: Namespace, term: Terminal) -> None:
        commands = term.parser.list_commands()
        if not ns.command:
            self.commands = [
                command.format_help() for command in commands
            ]
        else:
            self.commands = [
                command.format_help() for command in commands
                if command.name in ns.command
            ]

    def main(self, ns: Namespace, term: Terminal) -> None:
        return ('\n\n').join(self.commands)


def setup(parser: Parser) -> None:
    parser.add_command(Help())
