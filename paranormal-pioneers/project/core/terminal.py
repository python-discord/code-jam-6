from sys import stderr, stdin, stdout
from typing import IO, Optional, NoReturn

from project.core.constants import FILE_SYSTEM
from project.core.path import Path
from project.core.utils import FS
from project.core.parser import Parser

env = dict(
    name='name',
    term_name='term',
    ps='$',
    end=' ',
    format='{name}@{terminal}:{path}{ps}{end}',
)

rc = (Path(__file__).parent.parent / 'file_system' / '.termrc').resolve()

if rc.exists():
    exec(rc.read_text('utf-8'), env)


class Terminal:
    def __init__(
        self,
        io_in: IO = stdin,
        io_err: IO = stderr,
        io_out: IO = stdout,
        ps_format: str = '{name}@{terminal}:{path}{ps}{end}',
        name: str = 'root',
        term_name: str = 'term',
        end: str = ' ',
        ps: str = '$',
    ) -> None:
        # those are useless for now
        self._in = io_in
        self._err = io_err
        self._out = io_out

        # TODO: add config loading
        self._fs = FS()

        self._format = ps_format
        self._name = name
        self._term_name = term_name
        self._ps = ps
        self._end = end

        self._path: Path = Path(FILE_SYSTEM)

        self._parser = Parser()
        self._load_commands()

    @property
    def fs(self):
        return self._fs

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
    def end(self):
        return self._end

    @property
    def format(self) -> str:
        return self._format

    @property
    def path(self) -> Path:
        return self._path

    @property
    def parser(self) -> Parser:
        return self._parser

    def start(self) -> None:
        self.loop()

    def run_cmd(self, command: str) -> str:
        return self.parser.execute(command, self)

    def loop(self) -> NoReturn:
        # main loop here; we might change it soon.
        while True:

            # read, eval, print, loop
            ps = self.format_ps()
            command = input(ps)

            try:
                result = self.parser.execute(command, self)

            except BaseException as exc:
                if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                    raise

                print(f'{exc}')

            else:
                if result is not None:
                    print(result)

    def format_ps(self, end: Optional[str] = None) -> str:
        if end is None:
            end = self.end

        try:
            path = Path('~') / self.path.relative_to(FILE_SYSTEM)
        except ValueError:
            path = self.path

        return self.format.format(
            path=path, name=self.name, terminal=self.term, ps=self.ps, end=end
        )

    def _load_commands(self) -> None:
        for file in self.fs.resolve_commands():
            name = file.name.replace(file.suffix, str())
            self.parser.load_command(name)
