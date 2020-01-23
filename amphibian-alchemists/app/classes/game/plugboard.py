from kivy.factory import Factory
from kivy.properties import BoundedNumericProperty, DictProperty
from kivy.uix.screenmanager import Screen

from .save_game import save_plugs


class PlugboardScreen(Screen):
    plugs_in_screen = BoundedNumericProperty(0, min=0, max=20)
    all_plugged = []
    plug_reference = []
    wires = DictProperty({})
    wire_colors = (
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
        [128 / 255, 0, 128 / 255],
        [102 / 255, 128 / 255, 0],
        [55 / 255, 171 / 255, 200 / 255],
        [85 / 255, 0, 34 / 255],
        [1, 102 / 255, 0],
    )

    def get_plug(self, instance):
        if self.plugs_in_screen < self.property("plugs_in_screen").get_max(self):
            plug = Factory.Plug(
                size_hint=(None, None),
                size=self.ids.plug_board.plug_reference.size,
                pos=instance.pos,
            )
            self.ids.floating_widgets.add_widget(plug)
            self.all_plugged.append(instance.name)
            self.plug_reference.append(plug)
            if self.plugs_in_screen % 2 != 0:
                wire = Factory.Wire()
                wire.points = [
                    *self.ids.plug_board.ids[self.all_plugged[-2]].center,
                    *self.ids.plug_board.ids[self.all_plugged[-1]].center,
                ]
                wire.plugs = "".join(self.all_plugged[-2:])
                wire.color = self.wire_colors[int((len(self.all_plugged) / 2) % 13 - 1)]
                self.ids.floating_widgets.add_widget(wire)
                self.wires.update({wire.plugs: wire})
                self.ids.remove_plug.disabled = False
            else:
                self.ids.remove_plug.disabled = True
            self.plugs_in_screen += 1
            if len(self.all_plugged) % 2 == 0:
                save_plugs(self.all_plugged)

    def handle_plug_release(self, instance):
        if instance.name not in self.all_plugged:
            self.get_plug(instance)

    def remove_grouped_plugs(self):
        if self.plugs_in_screen >= 2 and self.plugs_in_screen % 2 == 0:
            self.ids.floating_widgets.remove_widget(self.plug_reference[-1])
            self.ids.floating_widgets.remove_widget(self.plug_reference[-2])
            wire_ref = "".join(self.all_plugged[-2:])
            self.ids.floating_widgets.remove_widget(self.wires[wire_ref])
            del self.wires[wire_ref]
            del self.plug_reference[-2:]
            del self.all_plugged[-2:]
            self.plugs_in_screen -= 2
            save_plugs(self.all_plugged)

    def on_plughole_recenter(self, instance, value):
        if self.manager.current == "plugboard_screen" and self.all_plugged:
            if instance.name in self.all_plugged:
                self.plug_reference[
                    self.all_plugged.index(instance.name)
                ].center = instance.center
                self.plug_reference[
                    self.all_plugged.index(instance.name)
                ].size = instance.size
                if self.wires:
                    for item in self.wires.keys():
                        if instance.name in item:
                            self.wires[item].points = (
                                *self.ids.plug_board.ids[item[0]].center,
                                *self.ids.plug_board.ids[item[1]].center,
                            )

    def check_plugs(self):
        """
        This method will check if there's an unpaired plug in the board.
        If so, then the plug will be deleted
        """
        if self.plugs_in_screen > 0 and self.plugs_in_screen % 2 != 0:
            self.ids.floating_widgets.remove_widget(self.plug_reference[-1])
            del self.plug_reference[-1]
            del self.all_plugged[-1]
            self.plugs_in_screen -= 1
            save_plugs(self.all_plugged)
