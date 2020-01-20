from kivy.animation import Animation
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, DictProperty
from kivy.uix.screenmanager import Screen


class PlugboardScreen(Screen):
    all_plugged = []
    plugs_in_screen = BoundedNumericProperty(0, min=0, max=20)
    last_plugs_count = 0
    wires = DictProperty({})

    def get_plug(self):
        if self.plugs_in_screen == self.property("plugs_in_screen").get_min(self):
            self.ids.remove_plug.text = "Drag the plug here to discard..."
        if self.plugs_in_screen < self.property("plugs_in_screen").get_max(self):
            plug = Factory.Plug(
                size_hint=(None, None),
                size=[
                    self.ids.plug_board.plug_reference.size[0] - dp(10),
                    self.ids.plug_board.plug_reference.size[1] - dp(10),
                ],
            )
            self.ids.floating_widgets.add_widget(plug)
            self.last_plugs_count = self.plugs_in_screen
            self.plugs_in_screen += 1

    def handle_touch_up(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.delete_from_pair(instance)
            if instance.collide_widget(self.ids.remove_plug):
                self.ids.floating_widgets.remove_widget(instance)
                self.last_plugs_count = self.plugs_in_screen
                self.plugs_in_screen -= 1

            for relativelayout in self.ids.plug_board.children:
                for child in relativelayout.children:
                    if isinstance(child, Factory.PlugHole) and instance.collide_widget(
                        child
                    ):
                        if child.name not in self.all_plugged:
                            instance.center = child.center
                            instance.plugged_in = child.name
                        else:
                            self.on_plugged_out(instance)
                        return

    def on_plugged_in(self, instance, value):
        self.all_plugged.clear()
        for plug in self.ids.floating_widgets.children:
            if isinstance(plug, Factory.Plug) and plug.plugged_in != "":
                self.all_plugged.append(plug.plugged_in)
        if len(self.all_plugged) >= 2 and len(self.all_plugged) % 2 == 0:
            wire = Factory.Wire()
            wire.points = [
                *self.ids.plug_board.ids[self.all_plugged[0]].center,
                *self.ids.plug_board.ids[self.all_plugged[1]].center,
            ]
            self.ids.floating_widgets.add_widget(wire)
            self.wires.update({f"{''.join(self.all_plugged[:2])}": wire})
            self.ids.floating_widgets.get_a_plug.disabled = False

    def on_plugged_out(self, instance):
        if instance.plugged_in in self.all_plugged:
            self.all_plugged.remove(instance.plugged_in)
            self.delete_from_pair(instance)
        instance.plugged_in == ""
        self.animate_positioning(instance)
        return True

    def animate_positioning(self, instance):
        anim = Animation(pos=[0, 0], duration=0.5)
        anim.start(instance)

    def delete_from_pair(self, instance):
        for item in self.wires.items():
            if instance.plugged_in in item[0]:
                self.ids.floating_widgets.remove_widget(self.wires[item[0]])
                del self.wires[item[0]]
                break

    def on_plugs_in_screen(self, instance, value):
        if value % 2 == 0:
            if self.last_plugs_count > self.plugs_in_screen:
                self.ids.floating_widgets.get_a_plug.disabled = False
            else:
                self.ids.floating_widgets.get_a_plug.disabled = True
        else:
            self.ids.floating_widgets.get_a_plug.disabled = False

    def on_plughole_recenter(self, instance, value):
        """This avoids to unplug everything when resizing"""
        # FIXME: avoid calling this when moving the widow.
        # It can be achieved using a RelativeLayout instead
        # of a FloatLayout, but breaks the handle_touch_up method
        if self.manager.current == "plugboard_screen" and self.all_plugged:
            for child in self.ids.floating_widgets.children:
                if (
                    isinstance(child, Factory.Plug)
                    and child.plugged_in == instance.name
                ):
                    child.center = instance.center
                else:
                    child.size = (
                        self.ids.plug_board.plug_reference.size[0] - dp(10),
                        self.ids.plug_board.plug_reference.size[1] - dp(10),
                    )
            for wire in self.wires.items():
                wire[1].points = [
                    *self.ids.plug_board.ids[wire[0][0]].center,
                    *self.ids.plug_board.ids[wire[0][1]].center,
                ]

    def handle_wire_pos(self, instance, touch):
        if self.collide_point(*touch.pos) and self.wires and instance.plugged_in:
            for item in self.wires.items():
                if instance.plugged_in in item[0]:
                    moving_plug = 0
                    if item[0].index(instance.plugged_in) != 0:
                        moving_plug = 2

                    item[1].points[moving_plug] = instance.center[0]
                    item[1].points[moving_plug + 1] = instance.center[1]
                    break
