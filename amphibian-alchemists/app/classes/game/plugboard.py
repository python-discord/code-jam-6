from kivy.factory import Factory
from kivy.properties import BoundedNumericProperty
from kivy.uix.screenmanager import Screen


class PlugboardScreen(Screen):
    all_plugged = []
    pairs_of_plugs = {}
    plugs_in_screen = BoundedNumericProperty(0, min=0, max=20)
    last_plugs_count = 0

    def get_plug(self):
        if self.plugs_in_screen == self.property("plugs_in_screen").get_min(self):
            self.ids.remove_plug.text = "Drag the plug here to discard..."
        if self.plugs_in_screen < self.property("plugs_in_screen").get_max(self):
            plug = Factory.Plug()
            self.ids.floating_widgets.add_widget(plug)
            self.last_plugs_count = self.plugs_in_screen
            self.plugs_in_screen += 1

    def handle_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if instance.collide_widget(self.ids.remove_plug):
                for item in self.pairs_of_plugs.items():
                    if instance.plugged_in in item[1]:
                        del self.pairs_of_plugs[item[0]]
                        break

                self.ids.floating_widgets.remove_widget(instance)
                self.last_plugs_count = self.plugs_in_screen
                self.plugs_in_screen -= 1

            for floatlayouts in self.ids.plug_board.children:
                for children in floatlayouts.children:
                    if instance.collide_widget(children) and type(children) == Factory.PlugHole:
                        if children.name not in self.all_plugged:
                            instance.center = children.center
                            instance.plugged_in = children.name
                        elif instance.plugged_in == children.name:
                            self.all_plugged.remove(instance.plugged_in)
                            instance.plugged_in == ""
                            instance.pos = [0, 0]
                        else:
                            instance.pos = [0, 0]
                        return

    def on_plugged_in(self, instance, value):
        self.all_plugged.clear()
        for plugs in self.ids.floating_widgets.children:
            if type(plugs) == Factory.Plug and plugs.plugged_in != "":
                self.all_plugged.append(plugs.plugged_in)
        if len(self.all_plugged) % 2 == 0:
            self.pairs_of_plugs.update(
                {
                    f"{self.all_plugged[0]}{self.all_plugged[1]}": [
                        self.all_plugged[0],
                        self.all_plugged[1],
                    ]
                }
            )
            self.ids.floating_widgets.get_a_plug.disabled = False

    def on_plugs_in_screen(self, instance, value):
        if value % 2 == 0:
            if self.last_plugs_count > self.plugs_in_screen:
                self.ids.floating_widgets.get_a_plug.disabled = False
            else:
                self.ids.floating_widgets.get_a_plug.disabled = True
        else:
            self.ids.floating_widgets.get_a_plug.disabled = False
