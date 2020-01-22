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
newline = "\n"

if __name__ == "__main__":
    with open("data/example_game_cards.json") as f:
        _cards = [Card(**card_dict) for card_dict in json.load(f)]
    with open("data/example_game_states.json") as f:
        _game_states = json.load(f)

    game = Game(_cards, _game_states)

    card = game.start_game()
    for _ in range(10):
        root_logger.debug(f"Card options: {card.options}")
        root_logger.info(f"Which option:")
        option = input(f"{newline.join(f'{i} {opt.text}' for i, opt in enumerate(card.options))}"
                       f"\nInput:")

        selected_option = card.options[int(option)]
        outcome = selected_option.get_outcome()
        root_logger.debug(f"Outcome of option: {outcome}")
        card = game.take_turn(outcome)
