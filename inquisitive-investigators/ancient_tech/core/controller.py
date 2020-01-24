from kivy.event import EventDispatcher

class Controller(EventDispatcher):
    __events__ = ('on_update', 'on_edit')
