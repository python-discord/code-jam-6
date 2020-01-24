from argparse import Namespace
from pathlib import PurePath
import os

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import PathLike, FS


class Mkdir(command.Command):
    """Create the DIRECTORY(ies), if they do not already exist."""
    def __init__(self) -> None:
        super().__init__(name='mkdir')

    def _resolve_path(self, cwd: PathLike, path: PathLike, filesystem: FS):
        """Make user provided path relative with current working directory."""
        path = PurePath(cwd) / path
        filesystem.check_env(path)
        return path

    @command.option('dir', nargs='+')
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        self.dirs = [self._resolve_path(term.path, dir, term.fs) for dir in ns.dir]

    def main(self, ns: Namespace, term: Terminal) -> None:
        for d in self.dirs:
            os.mkdir(d)


def setup(parser: Parser) -> None:
    parser.add_command(Mkdir())
