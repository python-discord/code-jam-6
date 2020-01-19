from project.core.terminal import IOTerminal
from project.core.api import SimpleBoot


if __name__ == '__main__':
    api = SimpleBoot().start()
    terminal = IOTerminal(api)
    terminal.start()
