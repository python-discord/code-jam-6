from argparse import ArgumentParser, Namespace
from types import FunctionType
from typing import Any, Callable, List, Tuple, Union

Function = Callable[[Any], Any]
Terminal = 'project.terminal.Terminal'


class PatchedParser(ArgumentParser):
    def exit(self, status: int = 0, message: str = ''):
        self._print_message(message)


class Option:
    def __init__(self, func, *args, **kwargs) -> None:

        if not isinstance(func, FunctionType):
            raise TypeError(f'Expected function, got type {type(func).__name__}.')

        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f'<Option func={self._func} args={self._args} kwargs={self._kwargs}>'

    def _call(self, *args, **kwargs) -> Any:
        return self._func(*args, **kwargs)

    def _expose_to(self, parser: ArgumentParser) -> None:
        parser.add_argument(*self._args, **self._kwargs)


def option(*args, **kwargs) -> Function:
    def wrapper(f: Function) -> Option:
        return Option(f, *args, **kwargs)
    return wrapper


class Command:
    def __init__(self, name: str) -> None:
        self._opt: List[Option] = []
        self._parser: PatchedParser = PatchedParser(prog=name, add_help=False)

        self._name: str = name

        self._make_args()

    def __repr__(self) -> str:
        return f'<Command {self.name}>'

    @property
    def name(self) -> str:
        return self._name

    @option('-h', '--help', action='store_true', default=False)
    def _help(self, ns: Namespace, term: Terminal) -> None:
        if ns.help:
            self._parser.print_help()

    def execute(self, term: Terminal, args: Union[str, List[str], Tuple[str]] = ()) -> Any:
        ns: Namespace = self._parse(args)

        for option in self._opt:
            option._call(self, ns=ns, term=term)

        if not ns.help:
            return self.main(ns=ns, term=term)

    def main(self, ns: Namespace, term: Terminal) -> Any:
        pass

    def _parse(self, args: Union[str, List[str]]) -> Namespace:
        if isinstance(args, str):
            args: List[str] = args.split()

        return self._parser.parse_args(args)

    def _make_args(self) -> None:
        for entry in dir(self):
            maybe_option = getattr(self, entry)
            if isinstance(maybe_option, Option):
                maybe_option._expose_to(self._parser)
                self._opt.append(maybe_option)
