import os

from kivy.app import App
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


class SelectableButton(RecycleDataViewBehavior, ToggleButton):
    def on_state(self, widget, value):
        game_selector_screen = App.get_running_app().root.get_screen(
            "game_selector_screen"
        )
        if value == "down":
            game_selector_screen.last_selected = widget.text
        else:
            game_selector_screen.last_selected = ""


class GameSelectorScreen(Screen):
    last_selected = StringProperty("")

    def on_enter(self, *args):
        if not os.path.exists(DATA_DIR):
            store = JsonStore(DATA_DIR)
            store.put("latest_game_id", id=None)
        self.populate()

    def populate(self):
        store = JsonStore(DATA_DIR)
        latest_game_id = store.get("latest_game_id")["id"]
        if latest_game_id is not None:
            for x in range(int(latest_game_id)):
                game = store.get(str(x))
                title = game["game_title"]
                created = str(game["created_date"])
                last_saved = str(game["last_saved_date"])
                self.rv.data.append(
                    {
                        "text": f"{title}\n"
                        f"Created: {created}\n"
                        f"Last Saved: {last_saved}"
                    }
                )
        else:
            self.rv.data = [{"text": "No saved games detected."}]

    def load_game(self, game):
        self.manager.current = "game_screen"
