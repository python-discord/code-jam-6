from pathlib import Path
from typing import Any, Dict, IO, Optional, NoReturn
from sys import stdin, stderr, stdout

from project.core.constants import BIN_DIR, FILE_SYSTEM
from project.core.parser import Parser


class Terminal:
    def __init__(
        self,
        io_in: IO = stdin,
        io_err: IO = stderr,
        io_out: IO = stdout,
        ps_format: str = '{name}@{terminal}:{path}{ps}',
        env: Optional[Dict[str, Any]] = None,
        name: str = 'root',
        term_name: str = 'term',
        path: str = FILE_SYSTEM,
        ps: str = '$',
    ) -> None:
        # those are useless for now
        self._in = io_in
        self._err = io_err
        self._out = io_out

        # TODO: add config loading
        self._format = ps_format
        self._name = name
        self._term_name = term_name
        self._ps = ps
        self._path: Path = Path(path)

        self._env = env or dict()
        self._parser = Parser()

    @property
    def env(self) -> Dict[str, Any]:
        return self._env

    @property
    def ps(self) -> str:
        return self._ps

    @property
    def name(self) -> str:
        return self._name

    @property
    def term(self) -> str:
        return self._term_name

    @property
    def format(self) -> str:
        return self._format

    @property
    def path(self) -> Path:
        return self._path

    @property
    def parser(self):
        return self._parser

    def start(self) -> None:
        self._prepare()
        self.loop()

    def loop(self) -> NoReturn:
        # main loop here; we might change it soon.
        while True:
            # read, eval, print, loop
            ps = self.format_ps(end=' ')
            command = input(ps)
            result = self.parser.execute(command, self)
            if result is not None:
                print(result)

    def format_ps(self, end: str = ''):
        return self.format.format(
            path=str(self.path).replace(str(FILE_SYSTEM), '~'),
            name=self.name,
            terminal=self.term,
            ps=self.ps,
        ) + end

    def _load_commands(self):
        for file in BIN_DIR.glob('*.py'):
            name = file.name.strip(file.suffix)
            self.parser.load_command(name)

    def _prepare(self):
        self._load_commands()
