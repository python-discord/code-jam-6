from typing import List

from TLOA.core.constants import (
    LIGHT_COLOR_MAX_RED, LIGHT_COLOR_MAX_GREEN, LIGHT_COLOR_MAX_BLUE,
    LIGHT_COLOR_MAX_ALPHA
)

from kivy.graphics import Mesh, Color
from kivy.vector import Vector
from kivy.clock import Clock


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
        self.time_to_focus = 5
        self.old_vertex3y_value = 0
        self.old_vertex4y_value = 0

        self.trace(point=point, surface=surface)

    def trace(self, point: Vector, surface: List[Vector]):
        # Compute the vertices for sun ray mesh
        self.mirror = surface
        self.point = point

        self.vertices = []

        self.indices = [0, 1, 2, 3]
        self.vertex1, self.vertex2, self.vertex3, self.vertex4 = self.mirror[1:]
        self.vertex3 = self.vertex3 + self.point
        self.vertex4 = self.vertex4 + self.point

        if self.target:
            # Make the light beam pointed to the target
            def start_focus(dt):
                self.vertices.extend([self.vertex1.x, self.vertex1.y,
                                      self.vertex2.x, self.vertex2.y])
                self.vertices.extend([self.vertex2.x, self.vertex2.y,
                                      self.vertex3.x, self.vertex3.y])
                self.vertices.extend([self.vertex3.x, self.vertex3.y +
                                      self.old_vertex3y_value, self.vertex4.x, self.vertex4.y])
                self.vertices.extend([self.vertex4.x, self.vertex4.y -
                                      self.old_vertex4y_value, self.vertex1.x, self.vertex1.y])
                self.time_to_focus -= 0.1
                self.old_vertex3y_value += 0.7
                self.old_vertex4y_value += 0.7

            if self.time_to_focus >= 5:
                self.time_to_focus -= 0.1
                self.event_focus = Clock.schedule_interval(start_focus, 0.01)

            if self.time_to_focus <= 0:
                Clock.unschedule(self.event_focus)
                self.indices = [0, 1, 2]
                vertex1, vertex2 = self.mirror[1:3]
                self.vertices.extend([self.point.x, self.point.y, vertex1.x, vertex1.y])
                self.vertices.extend([vertex1.x, vertex1.y, vertex2.x, vertex2.y])
                self.vertices.extend([vertex2.x, vertex2.y, self.point.x, self.point.y])

        else:
            # Make the light beam non-pointed when no target available
            self.old_vertex3y_value = 0
            self.old_vertex4y_value = 0
            self.time_to_focus = 5
            self.vertices.extend([self.vertex1.x, self.vertex1.y, self.vertex2.x, self.vertex2.y])
            self.vertices.extend([self.vertex2.x, self.vertex2.y, self.vertex3.x, self.vertex3.y])
            self.vertices.extend([self.vertex3.x, self.vertex3.y-15,
                                  self.vertex4.x, self.vertex4.y])
            self.vertices.extend([self.vertex4.x, self.vertex4.y+15,
                                  self.vertex1.x, self.vertex1.y])
