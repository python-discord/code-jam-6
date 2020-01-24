from kivy.graphics import Mesh, Color
from kivy.vector import Vector

from typing import List


class LightRays(Mesh):

    def __init__(self, point: Vector, surface: List[Vector], **kwargs):
        super(LightRays, self).__init__(**kwargs)
        self.color = Color(01.0, 0.98, 0.1, 0.65)
        self.vertices = []
        self.indices = []
        self.mode = 'traingle_fan'
        self.point = Vector(0,0)
        self.mirror = []

        self.trace(point=point, surface=surface)

    def trace(self, point: Vector, surface: List[Vector]):
        # Compute the vertices for sunray mesh 
        self.mirror = surface
        self.point = point

        vertex1, vertex2 = self.mirror[1:]
        self.indices = [0, 1, 2]
        self.vertices = []
        self.vertices.extend([self.point.x, self.point.y, vertex1.x, vertex1.y])
        self.vertices.extend([vertex1.x, vertex1.y, vertex2.x, vertex2.y])
        self.vertices.extend([vertex2.x, vertex2.y, self.point.x, self.point.y])
