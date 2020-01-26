from collections import defaultdict
from typing import Dict

from project.langs.brainfuck import getch

CHARS = '+-><[].,'


def brainfuck(code: str) -> None:
    """Evaluate brainfuck code."""
    code = cleanup(code)
    bracemap = build_bracemap(code)
    cells, codeptr, cellptr = defaultdict(int), 0, 0

    while codeptr < len(code):
        char = code[codeptr]

        if char == '+':
            cells[cellptr] += 1

        elif char == '-':
            cells[cellptr] -= 1

        elif char == '>':
            cellptr += 1

        elif char == '<':
            cellptr -= 1

        elif char == '[' and not cells[cellptr]:
            codeptr = bracemap[codeptr]

        elif char == ']' and cells[cellptr]:
            codeptr = bracemap[codeptr]

        elif char == '.':
            # TODO: change that to what we are going to use
            print(chr(cells[cellptr]), end='')

        elif char == ',':
            raise ValueError(", is not supported")
            cells[cellptr] = ord(getch.getch())

        codeptr += 1


def cleanup(code: str) -> str:
    return str().join(filter(lambda char: char in CHARS, code))


def build_bracemap(code: str) -> Dict[int, int]:
    temp_bracestack, bracemap = [], {}

    for position, char in enumerate(code):

        if char == '[':
            temp_bracestack.append(position)

        if char == ']':
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start

    return bracemap


def launch_repl() -> None:
    while True:
        try:
            code = input('brainfuck> ')

            if code.startswith(('exit', 'quit')):
                break

            brainfuck(code)
            print()

        except KeyboardInterrupt:
            break

        except Exception:
            print()
            print('error: execution failed')
