import sys
import json
import logging
from backend.main import Game
from backend.card_format import Card

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
root_logger.addHandler(handler)


if __name__ == "__main__":
    with open("data/example_game_cards.json") as f:
        _cards = [Card(**card_dict) for card_dict in json.load(f)]
    with open("data/example_game_states.json") as f:
        _game_states = json.load(f)

    game = Game(_cards, _game_states)

    card = game.start_game()
    for _ in range(10):
        option = input(f"Which option?\n"
                       f"{card.options}\nInput:")

        selected_option = card.options[0] if option == "1" else card.options[1]
        outcome = selected_option.get_outcome()
        root_logger.debug(f"Outcome of option: {outcome}")
        card = game.take_turn(outcome)
