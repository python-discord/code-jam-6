import os
from datetime import datetime
from random import sample
from string import ascii_uppercase

from enigma.machine import EnigmaMachine
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from requests import get

from .save_game import store_put, on_config_change

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


def get_wiki_summary() -> str:
    endpoint = (
        "https://en.wikipedia.org/w/api.php?action=query&list=random&"
        "format=json&rnnamespace=0&rnlimit=1&origin=*"
    )
    response = get(endpoint)
    title = (response.json())["query"]["random"][0]["title"]
    endpoint = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    response1 = get(endpoint + title.replace(" ", "%20"))
    return response1.json()["extract"]


def get_encrypted_text(text: str, rotor_settings: str, plug_settings: str) -> str:
    machine = EnigmaMachine.from_key_sheet(
        rotors="I II III",
        reflector="B",
        ring_settings=[1, 20, 11],
        plugboard_settings=plug_settings,
    )
    machine.set_display(rotor_settings)
    return machine.process_text(text)


def setup_new_game_settings():
    store = JsonStore(DATA_DIR)
    currrent_game_id = store.get("latest_game_id")["id"]
    if currrent_game_id is None:
        store.put("latest_game_id", id=0)
    else:
        store.put("latest_game_id", id=int(currrent_game_id) + 1)
    game_id = store.get("latest_game_id")["id"]
    App.get_running_app().game_id = game_id
    plug_array = sample(ascii_uppercase, 20)
    plugs = []
    for i in range(10):
        plugs.append("".join(plug_array[i * 2 : i * 2 + 2]))  # noqa
    plug_settings = " ".join(x for x in plugs)
    rotors = sample(ascii_uppercase, 3)
    rotor_setting = "".join(rotors)
    App.get_running_app().machine.from_key_sheet(
        rotors="I II III",
        reflector="B",
        ring_settings=[1, 20, 11],
        plugboard_settings=plug_settings,
    )
    App.get_running_app().machine.set_display(rotor_setting)

    """Storing data"""
    rotors.append(None)
    rotors.append(None)
    text = get_wiki_summary()
    store.put(
        game_id,
        game_title="Game {}".format(game_id),
        ciphered_text=get_encrypted_text(text, rotor_setting, plug_settings),
        unciphered_text=text,
        current_output_text="",
        last_saved_output_text="",
        created_date=datetime.now().isoformat(),
        last_saved_date=datetime.now().isoformat(),
        encrypted_state={"reflector": "B", "rotors": rotors, "plugs": plugs},
        current_state={
            "reflector": "B",
            "rotors": ["A", "A", "A", None, None],
            "plugs": ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"],
        },
        last_saved_state={
            "reflector": "B",
            "rotors": ["A", "A", "A", None, None],
            "plugs": ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"],
        },
    )


class GameScreen(Screen):
    """Do we automatically assume new game or should we save?"""

    Builder.load_file("kvs/game/enigmakeyboard.kv")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self._on_key_down)

    if not os.path.exists(DATA_DIR):
        store = JsonStore(DATA_DIR)
        store.put("latest_game_id", id=None)

    def on_enter(self, *args):
        store = JsonStore(DATA_DIR)
        # TODO Add load game screen and select a game id by
        #  running App.get_running_app().game_id = 0
        game_id = App.get_running_app().game_id
        if game_id is None or store.exists(str(App.get_running_app().game_id)) is False:
            setup_new_game_settings()
        else:
            on_config_change()

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        keys = {
            "q",
            "w",
            "e",
            "r",
            "t",
            "z",
            "u",
            "i",
            "o",
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "p",
            "y",
            "x",
            "c",
            "v",
            "b",
            "n",
            "m",
            "l",
        }
        if (
            self.manager.current == "game_screen"
            and codepoint in keys
            and self.ids.enigma_keyboard.ids.lamp_board.ids.board_input.focus
        ):
            self.ids.enigma_keyboard.ids.keyboard.ids[
                codepoint.upper()
            ].trigger_action()

    def handle_key(self, key):
        """
        Here goes what we're gonna do whenever a key in the machine is pressed
        """

        anim = Animation(_color=[1, 212 / 255, 42 / 255], duration=0.2) + Animation(
            _color=[1, 1, 1], duration=0.2
        )
        anim.start(self.ids.enigma_keyboard.ids.lamp_board.ids.lamp)

        board_input = self.ids.enigma_keyboard.ids.lamp_board.ids.board_input

        if not board_input.focus:
            board_input.insert_text(key.name)
        App.get_running_app().machine.key_press(key.name)
        store_put(current_output_text=board_input.text)

    def load_old_game(self):
        game_id = App.get_running_app().game_id
        store = JsonStore(DATA_DIR)
        game = store.get(str(game_id))
        store_put(
            last_saved_date=datetime.now().isoformat(),
            current_state=game["last_saved_state"],
            current_output_text=game["last_saved_output_text"],
        )

    def save_game(self):
        game_id = App.get_running_app().game_id
        store = JsonStore(DATA_DIR)
        game = store.get(str(game_id))
        store_put(
            last_saved_date=datetime.now().isoformat(),
            last_saved_state=game["current_state"],
            last_saved_output_text=game["current_output_text"],
        )

    def change_game_title(self, btn, title):
        if title != "" or title is not None:
            store_put(game_title=title)
