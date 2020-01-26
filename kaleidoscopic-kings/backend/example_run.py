import sys
import logging
from backend.main import load_game

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
root_logger.addHandler(handler)
newline = "\n"

if __name__ == "__main__":
    game = load_game()

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
        root_logger.debug(game.game_state.get_main_state(0))
