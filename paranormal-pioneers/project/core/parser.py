import importlib
from typing import Dict, List

from project.core.command import Command
from project.core.log import log

BIN_PATH = 'project.file_system.bin'
Terminal = 'project.terminal.Terminal'


class Parser:
    def __init__(self) -> None:
        self._commands: Dict[str, Command] = {}

    def add_command(self, command: Command) -> None:
        self._commands[command.name] = command

    def load_command(self, module: str, char: str = '.') -> None:
        path: str = make_path(module)

        try:
            module = importlib.import_module(path)  # type: ignore
        except ImportError:
            log.warning(f'Could not load command: {module!r}.')

        if not hasattr(module, 'setup'):
            log.warning(f'Command module does not have setup function: {module!r}.')
            return

        module.setup(self)

    def execute(self, string: str, term: Terminal) -> None:
        args: List[str] = string.split()

        if not args:
            return

        commands = self._commands
        command_name = args.pop(0)

        if command_name in commands:
            return commands.get(command_name).execute(term=term, args=args)

        log.warning(f'error: could not execute string: {string!r}')


def make_path(module: str) -> str:
    return ('.').join(BIN_PATH.split('.') + module.split('.'))
