from argparse import Namespace

from project.core import command
from project.core.log import log
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import check_env, find_dir, PathLike


class Cat(command.Command):
    def __init__(self):
        super().__init__(name='cat')

    def get_path(self, before: PathLike, after: PathLike) -> PathLike:
        path = find_dir(before, after)
        if not check_env(path):
            return before
        return path

    @command.option('path')
    def handle_path(self, ns: Namespace, term: Terminal) -> None:
        self.path = self.get_path(term.path, ns.path)

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            if ns.path is not None and self.path != term.path:
                if self.path.is_file():
                    return self.path.read_text('utf-8')
                log.warning('error: not a file')
        except OSError:
            log.warning('error: no such file')


def setup(parser: Parser) -> None:
    parser.add_command(Cat())
