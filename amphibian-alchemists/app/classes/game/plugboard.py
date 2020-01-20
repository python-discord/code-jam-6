from kivy.factory import Factory
from kivy.uix.screenmanager import Screen


class PlugboardScreen(Screen):
    plug_count = 0

    def plug_handler(self):
        print("CLICK")

    def get_plug(self):
        if self.plug_count == 0:
            self.ids.remove_plug.text = "Drag here to remove the plug..."
        if self.plug_count < 30:
            plug = Factory.Plug()
            self.ids.floating_widgets.add_widget(plug)

    def handle_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if instance.collide_widget(self.ids.remove_plug):
                self.ids.floating_widgets.remove_widget(instance)

            for floatlayouts in self.ids.plug_board.children:
                for children in floatlayouts.children:
                    if instance.collide_widget(children) and type(children) == Factory.PlugHole:
                        instance.center = children.center
                        break
