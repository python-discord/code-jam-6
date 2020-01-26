from argparse import Namespace
from datetime import datetime
from typing import Iterator, List

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal
from project.core.utils import PathLike

type_form = '<{}>'
time_form = '({}; {})'
size_form = '[{}]'
name_form = '{}'


class LS(command.Command):
    """List all files in a given directory.
    Example: ls -a -l ./bin
    """
    def __init__(self) -> None:
        super().__init__(name='ls')

    @command.option('dir', nargs='?', default='.')
    def handle_dir(self, ns: Namespace, term: Terminal) -> None:
        self.dir = term.fs.get_path(term.path, ns.dir)

    @command.option('-a', '--all', action='store_true', default=False)
    def handle_all(self, ns: Namespace, term: Terminal) -> None:
        self.show_all = ns.all

    @command.option('-l', '--long', action='store_true', default=False)
    def handle_long(self, ns: Namespace, term: Terminal) -> None:
        self.long = ns.long

    def main(self, ns: Namespace, term: Terminal) -> str:
        entries = []

        for path in sorted(term.fs.iter_dir(self.dir)):
            name = path.name

            if name.startswith('.') and not self.show_all:
                continue

            typeof = _define_type(path)

            if self.long:
                stat = path.stat()
                to_add = [
                    type_form.format(typeof),
                    time_form.format(
                        _human_timestamp(stat.st_ctime), _human_timestamp(stat.st_mtime)
                    ),
                    size_form.format(stat.st_size),
                    name_form.format(name),
                ]

            else:
                to_add = [type_form.format(typeof), name_form.format(name)]

            entries.append(to_add)

        return ('\n').join((' ').join(strings) for strings in expand(entries))


def setup(parser: Parser) -> None:
    parser.add_command(LS())


def _make(max_len: int, column: List[str], fill: str) -> Iterator[str]:
    return (string + (fill * (max_len - len(string))) for string in column)


def _gen(strings: List[List[str]], fill: str = ' ') -> Iterator[Iterator[str]]:
    for column in zip(*strings):
        yield _make(max(map(len, column)), column, fill)


def expand(strings: List[List[str]], fill: str = ' ') -> List[List[str]]:
    return zip(*_gen(strings, fill))


def _human_timestamp(seconds: int) -> str:
    return datetime.fromtimestamp(seconds).strftime('%y.%m.%d %H:%M:%S')


def _define_type(path: PathLike) -> str:
    if path.is_dir():
        return 'dir'
    elif path.is_socket():
        return 'socket'
    elif path.is_symlink():
        return 'link'
    else:
        return 'file'
