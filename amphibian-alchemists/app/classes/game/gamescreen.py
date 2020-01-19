import os
from random import sample
from string import ascii_uppercase

from enigma.machine import EnigmaMachine
from kivy.app import App
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from requests import get

DATA_DIR = os.path.join(
    App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json")
)


def on_config_change():
    """
    After you change the JSON data w/ JSONStore, call this function
    This should only be called for rotor or plug changes
    """
    store = JsonStore(DATA_DIR)
    game_id = str(App.get_running_app().game_id)
    plugs = store.get(game_id)["current_state"]["plugs"]
    plug_settings = " ".join(x for x in plugs)
    App.get_running_app().machine.from_key_sheet(
        rotors="I II III",
        reflector="B",
        ring_settings=[1, 20, 11],
        plugboard_settings=plug_settings,
    )
    rotors = ""
    for x in store.get(game_id)["current_state"]["rotors"]:
        if x is None:
            continue
        rotors = rotors.join(x)
    App.get_running_app().machine.set_display(rotors)


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
    # TODO UNTESTED!!!!!!!!
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
    plug_array = sample(ascii_uppercase, 20)
    plugs = []
    for i in range(10):
        plugs.append("".join(plug_array[i * 2:i * 2 + 2]))
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
        ciphered_text=get_encrypted_text(text, rotor_setting, plug_settings),
        unciphered_text=text,
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
