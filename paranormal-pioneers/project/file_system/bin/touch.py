from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import FS, OSException, PathLike


class Touch(command.Command):
    def __init__(self) -> None:
        super().__init__(name='touch')

    def get_path(self, before: PathLike, after: PathLike, fs: FS) -> PathLike:
        path = fs.find_dir(before, after)
        fs.check_env(path)
        return path

    @command.option('path')
    def handle_path(self, ns: Namespace, term: Terminal) -> None:
        self.path = self.get_path(term.path, ns.path, term.fs)

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            term.fs.touch(self.path)
        except OSError:
            raise OSException('error: no such file or directory') from None


def setup(parser: Parser) -> None:
    parser.add_command(Touch())
