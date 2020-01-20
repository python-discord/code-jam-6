import os
from datetime import datetime

from kivy.app import App
from kivy.storage.jsonstore import JsonStore

DATA_DIR = os.path.join(App.get_running_app().APP_DIR, os.path.normcase("data/gamestate.json"))


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


def load_old_game():
    game_id = App.get_running_app().game_id
    store = JsonStore(DATA_DIR)
    game = store.get(str(game_id))
    store_put(
        last_saved_date=datetime.now().isoformat(),
        current_state=game["last_saved_state"],
        current_output_text=game["last_saved_output_text"],
    )


def save_game(title: str = None):
    game_id = App.get_running_app().game_id
    store = JsonStore(DATA_DIR)
    game = store.get(str(game_id))
    store_put(
        game_title=title,
        last_saved_date=datetime.now().isoformat(),
        last_saved_state=game["current_state"],
        last_saved_output_text=game["current_outpust_text"],
    )
