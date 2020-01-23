import os

from kivy.app import App
from kivy.storage.jsonstore import JsonStore

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
        rotors += x
    App.get_running_app().machine.set_display(rotors)


def store_put(
    game_id=None,
    game_title: str = None,
    ciphered_text: str = None,
    unciphered_text: str = None,
    current_output_text: str = None,
    last_saved_output_text: str = None,
    created_date: str = None,
    last_saved_date: str = None,
    encrypted_state=None,
    current_state=None,
    last_saved_state=None,
):
    """Assumes game already started."""
    if game_id is None:
        game_id = str(App.get_running_app().game_id)
    store = JsonStore(DATA_DIR)
    game = store.get(str(game_id))
    if game_title is None:
        game_title = game["game_title"]
    if ciphered_text is None:
        ciphered_text = game["ciphered_text"]
    if unciphered_text is None:
        unciphered_text = game["unciphered_text"]
    if current_output_text is None:
        current_output_text = game["current_output_text"]
    if last_saved_output_text is None:
        last_saved_output_text = game["last_saved_output_text"]
    if created_date is None:
        created_date = game["created_date"]
    if last_saved_state is None:
        last_saved_state = game["last_saved_date"]
    if encrypted_state is None:
        encrypted_state = game["encrypted_state"]
    if current_state is None:
        current_state = game["current_state"]
    if last_saved_state is None:
        last_saved_state = game["last_saved_state"]
    store.put(
        str(game_id),
        game_title=game_title,
        ciphered_text=ciphered_text,
        unciphered_text=unciphered_text,
        current_output_text=current_output_text,
        last_saved_output_text=last_saved_output_text,
        created_date=created_date,
        last_saved_date=last_saved_date,
        encrypted_state=encrypted_state,
        current_state=current_state,
        last_saved_state=last_saved_state,
    )


def save_plugs(unfilter_plugs: list):
    plugs = []
    for x in range(int(len(unfilter_plugs) / 2)):
        plugs.append(unfilter_plugs[x * 2] + unfilter_plugs[x * 2 + 1])
    store = JsonStore(DATA_DIR)
    game_id = str(App.get_running_app().game_id)
    current_state = store.get(game_id)["current_state"]
    current_state["plugs"] = plugs
    store_put(current_state=current_state)
    on_config_change()


def save_rotors(one: str, two: str, three: str):
    store = JsonStore(DATA_DIR)
    game_id = str(App.get_running_app().game_id)
    current_state = store.get(game_id)["current_state"]
    current_state["rotors"] = [one, two, three, None, None]
    store_put(current_state=current_state)
    on_config_change()
