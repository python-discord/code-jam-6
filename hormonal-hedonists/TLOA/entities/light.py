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
        self.target = False

        self.trace(point=point, surface=surface)

    def trace(self, point: Vector, surface: List[Vector], angle=0):
        # Compute the vertices for sun ray mesh
        self.mirror = surface
        self.point = point

        self.vertices = []

        if self.target:
            self.indices = [0, 1, 2]
            vertex1, vertex2 = self.mirror[1:3]
            self.vertices.extend([self.point.x, self.point.y, vertex1.x, vertex1.y])
            self.vertices.extend([vertex1.x, vertex1.y, vertex2.x, vertex2.y])
            self.vertices.extend([vertex2.x, vertex2.y, self.point.x, self.point.y])

            self.color = Color(
                LIGHT_COLOR_MAX_RED,
                LIGHT_COLOR_MAX_GREEN,
                LIGHT_COLOR_MAX_BLUE,
                LIGHT_COLOR_MAX_ALPHA)
        else:
            self.indices = [0, 1, 2, 3]
            vertex1, vertex2, vertex3, vertex4 = self.mirror[1:]
            vertex3 = vertex3 + self.point
            vertex4 = vertex4 + self.point

            self.vertices.extend([vertex1.x, vertex1.y, vertex2.x, vertex2.y])
            self.vertices.extend([vertex2.x, vertex2.y, vertex3.x, vertex3.y])
            self.vertices.extend([vertex3.x, vertex3.y, vertex4.x, vertex4.y])
            self.vertices.extend([vertex4.x, vertex4.y, vertex1.x, vertex1.y])

            self.color = Color(
                LIGHT_COLOR_MAX_RED,
                LIGHT_COLOR_MAX_GREEN,
                LIGHT_COLOR_MAX_BLUE,
                LIGHT_COLOR_MAX_ALPHA*0.4)
