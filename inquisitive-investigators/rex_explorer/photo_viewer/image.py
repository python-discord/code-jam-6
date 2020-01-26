from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior

from ..utils.constants import KEYS


class DynamicImage(DragBehavior, Image):
    
    def __init__(self, *args, **kwargs):
        super(DynamicImage, self).__init__(*args, **kwargs)
        self._kb = Window.request_keyboard(None, self)
        self._kb.bind(on_key_down=self.on_key_down)

    def on_key_down(self, kb, key, text, modifiers):
        """
        Captures specific key presses
        and executes accordingly.
        """
        if key[0] in KEYS['esc']:
            self.parent.parent.parent.manager.current = 'browser'

        elif key[0] in KEYS['='] and 'ctrl' in modifiers:
            self.size[0] += 50
            self.size[1] += 50

        elif key[0] in KEYS['-'] and 'ctrl' in modifiers:

            if not (self.height <= 0 or self.width <= 0):
                self.size[0] -= 50
                self.size[1] -= 50

    def on_touch_down(self, touch):
        """
        Zooming using the mouse scroll wheel.
        """
        if touch.is_mouse_scrolling:

            if touch.button == 'scrollup':

                if not (self.height <= 0 or self.width <= 0):
                    self.size[0] -= 50
                    self.size[1] -= 50

            elif touch.button == 'scrolldown':
                self.size[0] += 50
                self.size[1] += 50

        return super(DynamicImage, self).on_touch_down(touch)
