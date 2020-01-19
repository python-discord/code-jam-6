from argparse import Namespace

from project.core import command
from project.core.api import Api, PathLike
from project.core.log import log
from project.core.parser import Parser
from project.core.terminal import IOTerminal


class Touch(command.Command):
    def __init__(self):
        super().__init__(name='touch')

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
            if ns.path is not None:
                self.path.touch()
        except OSError:
            log.warning('error: no such file or directory')


def setup(parser: Parser) -> None:
    parser.add_command(Touch())
