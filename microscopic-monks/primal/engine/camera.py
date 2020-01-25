from typing import Tuple
from kivy.graphics.transformation import Matrix
from kivy.graphics.context_instructions import MatrixInstruction, PushMatrix, PopMatrix


class Camera:
    def get_viewport(self) -> Tuple[int, int]:
        raise NotImplementedError

    def get_projection(self) -> Matrix:
        raise NotImplementedError


class OrthographicCamera(Camera):
    def __init__(self, canvas, viewport_width: int, viewport_height: int):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.pos_x = viewport_width / 2
        self.pos_y = viewport_height / 2
        self.zoom = 1.0

        self.canvas = canvas
        self.modelview_matrix = MatrixInstruction(Matrix(), 'modelview_mat')
        self.projection_matrix = MatrixInstruction(Matrix(), 'projection_mat')

        self.update()

    def get_viewport(self) -> Tuple[int, int]:
        return self.viewport_width, self.viewport_height

    def start_region(self):
        self.canvas.add(PushMatrix())
        self.canvas.add(self.modelview_matrix)
        self.canvas.add(PushMatrix())
        self.canvas.add(self.projection_matrix)

    def end_region(self):
        self.canvas.add(PopMatrix())
        self.canvas.add(PopMatrix())

    def set_position(self, x: float, y: float):
        self.pos_x = x
        self.pos_y = y

    def update(self, delta: float = 0.0):
        self.projection_matrix.matrix = self.get_projection()
        self.modelview_matrix.matrix = Matrix()

    def get_projection(self) -> Matrix:
        width = self.viewport_width / 2
        height = self.viewport_height / 2

        x = -self.pos_x
        y = -self.pos_y

        projection = Matrix()
        projection.view_clip(0, self.viewport_width, 0, self.viewport_height, -1.0, 1.0, 0)
        projection.scale(self.zoom, self.zoom, self.zoom)
        projection.translate(1 + x / width * self.zoom, 1 + y / height * self.zoom, 0)

        return projection

    def get_position_projection(self, pos):
        projection = self.get_projection()
        x, y = pos

        x, y, _ = projection.project(x, y, 0, Matrix(), projection, 0, 0, self.viewport_width, self.viewport_height)
        x -= self.viewport_width
        y -= self.viewport_height

        return -x, -y

    def set_zoom(self, zoom: float):
        self.zoom = zoom
