from argparse import Namespace
from pathlib import Path
import os

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import PathLike, FS


class Rmdir(command.Command):
    """Remove the DIRECTORY(ies), if they are empty."""
    def __init__(self) -> None:
        super().__init__(name='rmdir')

    def _resolve_path(self, cwd: PathLike, path: PathLike, filesystem: FS) -> Path:
        """Make user provided path relative with current working directory."""
        path = filesystem.find_dir(cwd, path)
        filesystem.check_env(path)
        return path

    @command.option('dir', nargs='+')
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        self.dirs = [self._resolve_path(term.path, dir, term.fs) for dir in ns.dir]

    def main(self, ns: Namespace, term: Terminal) -> None:
        for dir in self.dirs:
            os.rmdir(dir)


def setup(parser: Parser) -> None:
    parser.add_command(Rmdir())
