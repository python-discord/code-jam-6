import sys

try:
    # windows
    import msvcrt
    windows = True

except ImportError:
    # unix
    import termios
    import tty
    windows = False


def unix_getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return char


def windows_getch():
    return msvcrt.getch()


getch = (
    windows_getch if windows else unix_getch
)
