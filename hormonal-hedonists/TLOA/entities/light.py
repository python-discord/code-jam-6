from typing import List

from TLOA.core.constants import (
    LIGHT_COLOR_MAX_RED, LIGHT_COLOR_MAX_GREEN, LIGHT_COLOR_MAX_BLUE,
    LIGHT_COLOR_MAX_ALPHA
)

from kivy.graphics import Mesh, Color
from kivy.vector import Vector


class LightRays(Mesh):

    def __init__(self, point: Vector, surface: List[Vector], **kwargs):
        super(LightRays, self).__init__(**kwargs)

        self.color = Color(
            LIGHT_COLOR_MAX_RED,
            LIGHT_COLOR_MAX_GREEN,
            LIGHT_COLOR_MAX_BLUE,
            LIGHT_COLOR_MAX_ALPHA)
        self.vertices = []
        self.indices = []
        self.mode = 'triangle_fan'
        self.point = Vector(0, 0)
        self.mirror = []

        self.trace(point=point, surface=surface)

    def trace(self, point: Vector, surface: List[Vector]):
        # Compute the vertices for sun ray mesh
        self.mirror = surface
        self.point = point

        vertex1, vertex2 = self.mirror[1:]
        self.indices = [0, 1, 2]
        self.vertices = []
        self.vertices.extend([self.point.x, self.point.y, vertex1.x, vertex1.y])
        self.vertices.extend([vertex1.x, vertex1.y, vertex2.x, vertex2.y])
        self.vertices.extend([vertex2.x, vertex2.y, self.point.x, self.point.y])
