from kivy.event import EventDispatcher
from kivy.graphics.instructions import VertexInstruction


class Entity(EventDispatcher):
    shape: VertexInstruction = None
