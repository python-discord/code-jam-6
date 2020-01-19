from argparse import Namespace

from project.core import command
from project.core.api import Api, PathLike
from project.core.log import log
from project.core.parser import Parser
from project.core.terminal import IOTerminal


class Cat(command.Command):
    def __init__(self):
        super().__init__(name='cat')

    def get_path(self, before: PathLike, after: PathLike, api: Api) -> PathLike:
        path = api.find_dir(before, after)
        if not api.check_env(path):
            return before
        return path

    @command.option('path')
    def handle_path(self, ns: Namespace, term: IOTerminal) -> None:
        self.path = self.get_path(term.path, ns.path, term.api)

    def main(self, ns: Namespace, term: IOTerminal) -> None:
        try:
            if ns.path is not None and self.path != term.path:
                if term.api.is_file(self.path):
                    with term.api.open_file(self.path, 'r') as f:
                        return f.read()
                log.warning('error: not a file')
        except KeyError:
            log.warning('error: no such file')


def setup(parser: Parser) -> None:
    parser.add_command(Cat())
