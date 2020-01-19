from argparse import Namespace
from datetime import datetime
from typing import Iterator, List

from project.core import command, api
from project.core.parser import Parser
from project.core.terminal import IOTerminal

type_form = '<{}>'
time_form = '({}; {})'
size_form = '[{}]'
name_form = '{}'


class LS(command.Command):
    def __init__(self):
        super().__init__(name='ls')

    @command.option('dir', nargs='?', default='.')
    def handle_dir(self, ns: Namespace, term: IOTerminal) -> None:
        self.dir = term.api.change_dir(term.path, ns.dir)

    @command.option('-a', '--all', action='store_true', default=False)
    def handle_all(self, ns: Namespace, term: IOTerminal) -> None:
        self.show_all = ns.all

    @command.option('-l', '--long', action='store_true', default=False)
    def handle_long(self, ns: Namespace, term: IOTerminal) -> None:
        self.long = ns.long

    def main(self, ns: Namespace, term: IOTerminal) -> str:
        entries = []

        for path in sorted(self.dir.iterdir()):
            name = path.name

            if name.startswith('.') and not self.show_all:
                continue

            typeof = _define_type(path)

            if self.long:
                stat = path.stat()
                to_add = [
                    type_form.format(typeof),
                    time_form.format(
                        _human_timestamp(stat.st_ctime),
                        _human_timestamp(stat.st_mtime)
                    ),
                    size_form.format(stat.st_size),
                    name_form.format(name)
                ]

            else:
                to_add = [
                    type_form.format(typeof),
                    name_form.format(name)
                ]

            entries.append(to_add)

        return ('\n').join((' ').join(strings) for strings in expand(entries))


def setup(parser: Parser) -> None:
    parser.add_command(LS())


def _make(max_len: int, column: List[str], fill: str) -> Iterator[str]:
    return (string + (fill * (max_len - len(string))) for string in column)


def _gen(strings: List[List[str]], fill: str = ' ') -> Iterator[Iterator[str]]:
    for column in zip(*strings):
        yield _make(max(map(lambda string: len(string), column)), column, fill)


def expand(strings: List[List[str]], fill: str = ' ') -> List[List[str]]:
    return zip(*_gen(strings, fill))


def _human_timestamp(seconds: int) -> str:
    return datetime.fromtimestamp(seconds).strftime('%y.%m.%d %H:%M:%S')


def _define_type(path: api.PathLike) -> str:
    if path.is_dir():
        return 'dir'
    elif path.is_socket():
        return 'socket'
    elif path.is_symlink():
        return 'link'
    else:
        return 'file'
