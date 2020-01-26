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
CONFIG_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gameconfig.json")
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
        store = JsonStore(DATA_DIR)
        if not os.path.exists(DATA_DIR) or store.count() == 0:
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
                try:
                    last_saved = datetime.fromisoformat(str(game["last_saved_date"]))
                    last_saved = last_saved.strftime(DATE_FORMAT)
                except ValueError:
                    # Since last_saved_time is None to begin with
                    last_saved = str(game["last_saved_date"]) or "None"
                self.rv.data.append(
                    {
                        "text": f"{title}\n"
                        f"Created: {created}\n"
                        f"Last Saved: {last_saved}"
                    }
                )
        else:
            self.rv.data = [{"text": self.no_saved_games}]

    def new_game(self):

        App.get_running_app().game_id = None
        self.manager.get_screen("rotor_screen").reset_rotors()
        self.manager.get_screen(
            "game_screen"
        ).ids.enigma_keyboard.ids.lamp_board.ids.board_output.text = ""
        self.manager.get_screen("plugboard_screen").clear_plugs()

        config_store = JsonStore(CONFIG_DIR)

        if (
            config_store.exists("auto_input")
            and config_store.get("auto_input")["value"] == 0
        ):
            self.manager.get_screen("game_screen").current_time = "200"
        else:
            self.manager.get_screen("game_screen").current_time = "100"

        self.manager.current = "game_screen"

    def load_game(self, game_index):
        App.get_running_app().game_id = int(game_index)
        self.manager.get_screen("rotor_screen").load_rotors()
        self.manager.get_screen("plugboard_screen").load_plugs()
        self.manager.get_screen("game_screen").load_output_text()

        self.manager.get_screen("game_screen").current_time = "100"

        self.manager.current = "game_screen"
