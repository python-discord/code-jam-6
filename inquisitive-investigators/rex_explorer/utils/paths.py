from pathlib import Path

BASE = Path('rex_explorer')


CORE = BASE / 'core'
EDITOR = BASE / 'editor'
FOOTER = BASE / 'footer'
MANAGER = BASE / 'manager'
PHOTO_VIEWER = BASE / 'photo_viewer'
STATIC = BASE / 'static'
TERMINAL = BASE / 'terminal'
UTILS = BASE / 'utils'


ICON = str(STATIC / 'icon.ico')
FONT = str(STATIC / 'retro_font')
ABOUT = str(STATIC / 'about.txt')
BUTTON = str(STATIC / 'blue.png')


CORE_KV = str(CORE / 'core.kv')
EDITOR_KV = str(EDITOR / 'editor.kv')
FOOTER_KV = str(FOOTER / 'footer.kv')
MANAGER_KV = str(MANAGER / 'filemanager.kv')
PHOTO_VIEWER_KV = str(PHOTO_VIEWER / 'viewer.kv')
TERMINAL_KV = str(TERMINAL / 'terminal.kv')
