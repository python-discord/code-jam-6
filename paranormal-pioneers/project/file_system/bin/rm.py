from argparse import Namespace
import os

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import PathLike, FS


class RM(command.Command):
    """Remove (unlink) the FILE(s)."""
    def __init__(self) -> None:
        super().__init__(name='rm')

    def _resolve_path(self, cwd: PathLike, path: PathLike, filesystem: FS):
        """Make user provided path relative with current working directory."""
        path = filesystem.find_dir(cwd, path)
        filesystem.check_env(path)
        return path

    @command.option('file', nargs='+')
    def handle_file(self, ns: Namespace, term: Terminal) -> None:
        self.files = [self._resolve_path(term.path, file, term.fs) for file in ns.file]

    def main(self, ns: Namespace, term: Terminal) -> None:
        for f in self.files:
            os.remove(f)


def setup(parser: Parser) -> None:
    parser.add_command(RM())
