import math

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle


class RepeatingBackground:
    """Inherit this mixin to easily support repeating background in a widget."""

    def setup_background(self, bg_image, delay=0, color=(1, 1, 1, 1)):
        """Setup the repeating background.

        This function must be called after a widget is initialized.

        :param bg_image: Path to the image used for the background
        :type bg_image: str
        :param delay: Delay of the resize event, defaults to 0
        :type delay: float, optional
        :param color: Colorization of bg_image, defaults to (1, 1, 1, 1)
            If color is (1, 1, 1, 1), the original colors of bg_image will be displayed.
        :type color: Tuple[float, float, float, float], optional
        """
        self.delay = delay

        texture = CoreImage(bg_image).texture
        texture.wrap = "repeat"

        with self.canvas.before:
            Color(*color)
            self.bg_rect = Rectangle(texture=texture)

        self.resize_event = Clock.schedule_once(lambda dt: None, 0)
        self.bind(size=self._delayed_resize, pos=self._delayed_resize)

    def _get_uvsize(self):
        texture = self.bg_rect.texture
        return (
            math.ceil(self.width / texture.width),
            math.ceil(self.height / texture.height)
        )

    def _get_background_size(self):
        texture = self.bg_rect.texture
        uv_width, uv_height = texture.uvsize
        return (uv_width * texture.width, uv_height * texture.height)

    def update_background(self, instance, value):
        """Update background size.

        This function does not need to be called if :meth:`mixins.RepeatingBackground.resize`
        is not overriden.
        """
        self.bg_rect.texture.uvsize = self._get_uvsize()
        self.bg_rect.texture = self.bg_rect.texture  # required to trigger update
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = self._get_background_size()

    def _delayed_resize(self, instance, value):
        if self.delay > 0:
            self.resize_event.cancel()
            self.resize_event = Clock.schedule_once(lambda dt: self.resize(instance, value), self.delay)
        else:
            self.resize(instance, value)

    def resize(self, instance, value):
        """Overide this method if needed."""
        self.update_background(instance, value)