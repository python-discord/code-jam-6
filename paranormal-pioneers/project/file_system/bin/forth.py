from argparse import Namespace
from pathlib import Path

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


def setup(parser: Parser) -> None:
    parser.add_command(Forth())


class Forth(command.Command):
    """
    Forth launcher
    examples:
        forth ." Hello World" ( prints hello world)
        forth -f source.forth ( evaluates the source.forth file)
        forth ." Hello world" -f source.forth ( evaluates the source.forth file and then prints hello world)
    """

    def __init__(self) -> None:
        super().__init__(name='forth')

    @command.option('-f', '--file', nargs='?', default=None,
                    help="the file passed will be evaluated and no repl will start, unless the i flag is present")
    def handle_file(self, ns: Namespace, term: Terminal) -> None:
        if ns.file:
            self.file: Path = term.fs.get_path(term.path, ns.file, check_dir=False)
        else:
            self.file = None

    @command.option('command', nargs='*', default='',
                    help="the forth line to execute")
    def handle_n(self, ns: Namespace, term: Terminal):
        self.i = ' '.join( ns.command )

    def main(self, ns: Namespace, term: Terminal) -> None:
        from project.langs.forth import forthimpl
        import sys
        import io
        og = sys.stdout
        new = sys.stdout = io.StringIO()
        env: forthimpl.ForthEnv = forthimpl.create_forth()
        if self.file:
            with self.file.open() as f:
                env.eval(f.read())
        env.eval(self.i)
        sys.stdout = og
        return new.getvalue()
