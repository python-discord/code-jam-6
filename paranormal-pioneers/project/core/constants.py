from project.core.path import Path

CANNOT_EXIT_ENV = True

ROOT = Path(__file__).parent.parent

FILE_SYSTEM = ROOT / 'file_system'
BIN_DIR = FILE_SYSTEM / 'bin'
