import io
import sys
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
        bf +++++++++++++. ( prints a newline )
        bf -f source.bf ( evaluates the source.bf file )
    """

    def __init__(self) -> None:
        super().__init__(name='bf')

    @command.option('-f', '--file', nargs='?', default=None,
                    help="the file to evaluate")
    def handle_file(self, ns: Namespace, term: Terminal) -> None:
        if ns.file:
            self.file: Path = term.fs.get_path(term.path, ns.file, check_dir=False)
        else:
            self.file = None

    @command.option('command', nargs='*', default='',
                    help="the bf line to execute")
    def handle_n(self, ns: Namespace, term: Terminal):
        self.i = ''.join(ns.command)

    def main(self, ns: Namespace, term: Terminal) -> None:
        from project.langs import brainfuck, bf_repl
        og = sys.stdout
        new = sys.stdout = io.StringIO()
        if self.file:
            with self.file.open() as f:
                read = f.read()
                brainfuck(read)
        if self.i:
            brainfuck(self.i)
        elif not self.file:
            print('please either provide a file or an input')
        sys.stdout = og
        return new.getvalue()

