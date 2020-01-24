from kivy.graphics import Mesh, Color
from kivy.vector import Vector

from typing import List
from itertools import combinations


class LightRays(Mesh):

    def __init__(self, **kwargs):
        super(LightRays, self).__init__(**kwargs)
        self.color: Color = Color(01.0, 0.98, 0.1, 0.65)
        self.vertices: List
        self.indices: List
        self.mode: str = 'traingle_fan'
        self.point: Vector
        self.mirror: List[Vector]

    def trace(self, point: Vector, surface: List[Vector]):
        # Compute the vertices for sunray mesh 
        self.mirror = surface
        self.point = point

        vertex1, vertex2 = self.mirror[1:]
        self.indices = [0, 1, 2]
        self.vertices = []
        for edge in combinations([self.point, vertex1, vertex2], 2):
            self.vertices.extend([edge[0].x, edge[0].y, edge[1].x, edge[1].y])
