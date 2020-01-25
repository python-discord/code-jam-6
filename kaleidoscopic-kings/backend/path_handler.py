from pathlib import Path


_BASE_DIR = Path(__file__).resolve().parent.parent
_DATA_DIR = "game_data"

_CARD_ART_DIR = "CardArt"
_GAME_ART_DIR = "GameArt"
_SOUNDS_DIR = "Sounds"
_STORY_DIR = "Story"

_CARDS_FILENAME = "game_cards.json"
_STATES_FILENAME = "game_states.json"
_GAME_GLOBALS_FILENAME = "game_globals.json"


def get_cards_json_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _STORY_DIR, _CARDS_FILENAME)


def get_game_state_json_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _STORY_DIR, _STATES_FILENAME)


def get_global_game_state_json_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _STORY_DIR, _GAME_GLOBALS_FILENAME)


def get_game_asset_directory_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name)


def get_card_art_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _CARD_ART_DIR)


def get_game_art_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _GAME_ART_DIR)


def get_game_sounds_path(game_story_name: str):
    return _BASE_DIR.joinpath(_DATA_DIR, game_story_name, _SOUNDS_DIR)
