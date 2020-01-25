import os

from kivy.app import App
from kivy.factory import Factory
from kivy.properties import BoundedNumericProperty, DictProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

from .save_game import save_plugs

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


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

    # Adding the plug (which is the plughole instance)
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
                # Adding the wire
                wire.plugs = "".join(self.all_plugged[-2:])
                wire.color = self.wire_colors[int((len(self.all_plugged) / 2) % 13 - 1)]
                # Configuring UI data
                self.ids.floating_widgets.add_widget(wire)
                self.wires.update({wire.plugs: wire})
                self.ids.remove_plug.disabled = False
            else:
                self.ids.remove_plug.disabled = True
            self.plugs_in_screen += 1

    # User clicks on the a button hole, which communicates to here
    def handle_plug_release(self, instance):
        # Checks the there is no plug here
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

    def remove_single_plug(self):
        if self.plugs_in_screen > 0 and self.plugs_in_screen % 2 != 0:
            self.ids.floating_widgets.remove_widget(self.plug_reference[-1])
            del self.plug_reference[-1]
            del self.all_plugged[-1]
            self.plugs_in_screen -= 1
            self.ids.remove_plug.disabled = False

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

    def on_leave(self):
        self.remove_single_plug()
        save_plugs(self.all_plugged)

    def clear_plugs(self):
        if self.plugs_in_screen % 2 != 0:
            self.remove_single_plug()
        else:
            for _ in range(self.plugs_in_screen // 2):
                self.remove_grouped_plugs()

    def load_plugs(self):
        if self.all_plugged:
            self.clear_plugs()
        # Prepare data
        store = JsonStore(DATA_DIR)
        plugs = store.get(str(App.get_running_app().game_id))["current_state"]["plugs"]
        # Assumes the data plugs are even. If game goes well
        # If not, we pop the last one.
        if len("".join(i for i in plugs)) % 2 != 0:
            new_plugs = []
            for x in plugs:
                new_plugs.append(str(x)[0])
                new_plugs.append(str(x)[1])
            # save_plugs(new_plugs)
            # Reset plugs to be the new even numbered length
            plugs = store.get(str(App.get_running_app().game_id))["current_state"][
                "plugs"
            ]

        """
        Begin creation of plugs
        We have to use get_plug method.
        We have to find all PlugHole instances
        """
        plugholes_instances = self.ids.plug_board.ids
        # Plugs prepared. Select instances. Adding in.
        for x in plugs:
            instance1 = plugholes_instances[str(x)[0]]
            instance2 = plugholes_instances[str(x)[1]]
            self.handle_plug_release(instance1)
            self.handle_plug_release(instance2)
