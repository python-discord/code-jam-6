from argparse import Namespace
from time import sleep

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


class Sleep(command.Command):
    """Sleep for X seconds.
    Example: sleep 13.01
    """
    def __init__(self) -> None:
        super().__init__(name='sleep')

    @command.option('delay', nargs='?', type=float, default=0)
    def handle_text(self, ns: Namespace, term: Terminal) -> None:
        self.delay = ns.delay

    def main(self, ns: Namespace, term: Terminal) -> str:
        try:
            sleep(self.delay)
        except KeyboardInterrupt:
            return


def setup(parser: Parser) -> None:
    parser.add_command(Sleep())