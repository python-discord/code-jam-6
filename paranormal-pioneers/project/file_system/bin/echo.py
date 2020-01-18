from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Echo(command.Command):
    def __init__(self):
        super().__init__(name='echo')

    @command.option('text', nargs='*')
    def handle_text(self, ns: Namespace, term: Terminal) -> None:
        self.text = (' ').join(ns.text)

    def main(self, ns: Namespace, term: Terminal) -> str:
        return self.text


def setup(parser: Parser) -> None:
    parser.add_command(Echo())
