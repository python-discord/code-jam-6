from argparse import Namespace

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import OSException


class MV(command.Command):
    """Move or rename a file/directory."""
    def __init__(self) -> None:
        super().__init__(name='mv')

    @command.option('paths', nargs='*')
    def handle_paths(self, ns: Namespace, term: Terminal) -> None:
        paths = ns.paths.copy()

        if len(paths) < 2:
            raise OSException('error: not enough paths given')

        self.dest = term.fs.get_path(term.path, paths.pop(), check_existing=False)

        self.srcs = list(
            term.fs.get_path(term.path, path, check_dir=False)
            for path in paths
        )

    def main(self, ns: Namespace, term: Terminal) -> None:
        try:
            if self.dest.is_dir():
                for src in self.srcs:
                    src.rename(self.dest / src.name)
            else:
                # rename attempt
                src = self.srcs.pop()
                if self.srcs:
                    raise OSException('error: cannot rename several files')

                src.rename(self.dest)
        except OSError:
            raise OSException('error: failed to move/rename paths')


def setup(parser: Parser) -> None:
    parser.add_command(MV())
