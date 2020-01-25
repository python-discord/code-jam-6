import os
from datetime import datetime

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class SelectableButton(RecycleDataViewBehavior, ToggleButton):
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_state(self, widget, value):
        game_selector_screen = App.get_running_app().root.get_screen(
            "game_selector_screen"
        )
        if value == "down" and widget.text != game_selector_screen.no_saved_games:
            game_selector_screen.last_selected = widget
        else:
            game_selector_screen.last_selected = None


class GameSelectorScreen(Screen):
    last_selected = ObjectProperty(None, allownone=True)
    no_saved_games = "No saved games found"

    def on_enter(self, *args):
        if not os.path.exists(DATA_DIR):
            store = JsonStore(DATA_DIR)
            store.put("latest_game_id", id=None)
        App.get_running_app().game_id = None
        self.rv.data = []
        self.populate()

    def populate(self):
        store = JsonStore(DATA_DIR)
        latest_game_id = store.get("latest_game_id")["id"]
        if latest_game_id is not None:
            for x in range(int(latest_game_id) + 1):
                game = store.get(str(x))
                title = game["game_title"]
                DATE_FORMAT = "%b %d %Y %H:%M:%S"
                created = datetime.fromisoformat(str(game["created_date"]))
                created = created.strftime(DATE_FORMAT)
                last_saved = datetime.fromisoformat(str(game["last_saved_date"]))
                last_saved = last_saved.strftime(DATE_FORMAT)
                self.rv.data.append(
                    {
                        "text": f"{title}\n"
                        f"Created: {created}\n"
                        f"Last Saved: {last_saved}"
                    }
                )
        else:
            self.rv.data = [{"text": self.no_saved_games}]

    def load_game(self, game):
        App.get_running_app().game_id = int(game.index)

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
        plugboard_screen = self.manager.get_screen("plugboard_screen")
        plugholes_instances = plugboard_screen.ids.plug_board.ids
        # Plugs prepared. Select instances. Adding in.
        for x in plugs:
            instance1 = plugholes_instances[str(x)[0]]
            instance2 = plugholes_instances[str(x)[1]]
            plugboard_screen.handle_plug_release(instance1)
            plugboard_screen.handle_plug_release(instance2)

        self.manager.current = "game_screen"
