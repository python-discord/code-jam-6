from argparse import Namespace
from pathlib import Path, PurePath

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import PathLike, FS


class MV(command.Command):
    """Move (rename) files."""
    def __init__(self) -> None:
        super().__init__(name='mv')

    def _resolve_path(self, cwd: PathLike, path: PathLike, filesystem: FS) -> PurePath:
        """Make user provided path relative with current working directory."""
        path = PurePath(cwd) / path
        filesystem.check_env(path)
        return path

    @command.option('source')
    def handle_1source(self, ns: Namespace, term: Terminal) -> None:
        self.source = Path(self._resolve_path(term.path, Path(ns.source), term.fs))

    @command.option('destination')
    def handle_2dest(self, ns: Namespace, term: Terminal) -> None:
        self.dest = self._resolve_path(term.path, ns.destination, term.fs)

    def main(self, ns: Namespace, term: Terminal) -> None:
        self.source.rename(self.dest)


def setup(parser: Parser) -> None:
    parser.add_command(MV())
