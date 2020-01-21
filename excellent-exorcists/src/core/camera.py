from typing import Tuple
from kivy.graphics.transformation import Matrix


class Camera:
    def get_viewport(self) -> Tuple[int, int]:
        raise NotImplementedError

    def get_projection(self) -> Tuple[Matrix, Matrix]:
        raise NotImplementedError


class OrthographicCamera(Camera):
    def __init__(self, viewport_width: int, viewport_height: int):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.aspect_ratio = float(viewport_height) / float(viewport_width)

        self.height = viewport_height
        self.width = viewport_width
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.zoom = 0

    def get_viewport(self) -> Tuple[int, int]:
        return self.viewport_width, self.viewport_height

    def set_size(self, width: int, height: int):
        self.height = height
        self.width = width

    def set_position(self, x: float, y: float):
        self.pos_x = x
        self.pos_y = y

    def update(self, delta: float):
        pass

    def set_zoom(self, zoom: float):
        self.zoom = zoom

    def get_projection(self) -> Tuple[Matrix, Matrix]:
        viewport_w = self.viewport_width
        viewport_h = self.viewport_height
        width = viewport_w / 2
        height = viewport_h / 2

        x = -self.pos_x
        y = -self.pos_y

        projection = Matrix()
        projection.view_clip(0, viewport_w, 0, viewport_h, -1.0, 1.0, 0)
        projection.scale(self.zoom, self.zoom, self.zoom)
        projection.translate(1 + x / width * self.zoom, 1 + y / height * self.zoom, 0)

        model_view = Matrix()

        return projection, model_view
