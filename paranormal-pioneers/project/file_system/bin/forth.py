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
        forth ( starts the forth repl )
        forth -f source.forth ( evaluates the source.forth file )
        forth -if source.forth ( evaluates the source.forth file and starts the repl )
    """


    def __init__(self) -> None:
        super().__init__(name='forth')

    @command.option('file', nargs='?', default=None,
                    help="the file passed will be evaluated and no repl will start, unless the i flag is present")
    def handle_file(self, ns: Namespace, term: Terminal) -> None:
        if ns.file:
            self.file: Path = term.fs.get_path(term.path, ns.file, check_dir=False)
        else:
            self.file = None

    @command.option('-i', '--interactive', action='store_true', default=False,
                    help="regardless of whether a file was passed, start the repl  after loading the file")
    def handle_n(self, ns: Namespace, term: Terminal):
        self.i = ns.interactive

    def main(self, ns: Namespace, term: Terminal) -> None:
        from project.langs.forth import forthimpl
        if self.file:
            with self.file.open() as f:
                env: forthimpl.ForthEnv = forthimpl.create_forth()
                env.eval(f.read())
                if self.i:
                    forthimpl.launch_repl(env)
        else:
            forthimpl.launch_repl()
