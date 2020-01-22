from kivy.graphics.instructions import VertexInstruction
from kivy.event import EventDispatcher


class Entity(EventDispatcher):
    shape: VertexInstruction = None
