from kivy.core.window import Keyboard


KEY_UP = Keyboard.keycodes['w']
KEY_DOWN = Keyboard.keycodes['s']
KEY_LEFT = Keyboard.keycodes['a']
KEY_RIGHT = Keyboard.keycodes['d']


NUMERIC_KEYS = []
for i in range(1, 11):
    NUMERIC_KEYS.append(Keyboard.keycodes[str(i % 10)])
