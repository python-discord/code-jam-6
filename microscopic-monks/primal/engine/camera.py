from typing import Tuple
from kivy.graphics.transformation import Matrix


class Camera:
    def get_viewport(self) -> Tuple[int, int]:
        raise NotImplementedError

    def get_projection(self) -> Matrix:
        raise NotImplementedError


class OrthographicCamera(Camera):
    def __init__(self, viewport_width: int, viewport_height: int):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.pos_x = 0.0
        self.pos_y = 0.0
        self.zoom = 1.0

    def get_viewport(self) -> Tuple[int, int]:
        return self.viewport_width, self.viewport_height

    def set_position(self, x: float, y: float):
        self.pos_x = x
        self.pos_y = y

    def update(self, delta: float):
        pass

    def set_zoom(self, zoom: float):
        self.zoom = zoom

    def get_projection(self):
        width = self.viewport_width / 2
        height = self.viewport_height / 2

        x = -self.pos_x
        y = -self.pos_y

        projection = Matrix()
        projection.view_clip(0, self.viewport_width, 0, self.viewport_height, -1.0, 1.0, 0)
        projection.scale(self.zoom, self.zoom, self.zoom)
        projection.translate(1 + x / width * self.zoom, 1 + y / height * self.zoom, 0)

        model_view = Matrix()

        return projection, model_view
