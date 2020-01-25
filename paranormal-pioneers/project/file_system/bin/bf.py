from argparse import Namespace
from pathlib import Path

from project.core import command
from project.core.parser import Parser
from project.core.terminal import Terminal


def setup(parser: Parser) -> None:
    parser.add_command(BrainFuck())


class BrainFuck(command.Command):
    """
    Brainfuck launcher
    examples:
        bf ( starts the Brainfuck repl )
        bf -f source.forth ( evaluates the source.bf file )
        bf -if source.forth ( evaluates the source.bf file and starts the repl )
    """

    def __init__(self) -> None:
        super().__init__(name='bf')

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
        from project.langs import brainfuck, bf_repl
        if self.file:
            with self.file.open() as f:
                read = f.read()
                brainfuck(read)
                if self.i:
                    bf_repl()
        else:
            bf_repl()
