import sys
import json
import random
from typing import List, Union
import logging
from backend.card_format import Card, GameStateHandler

logger = logging.getLogger(__name__)

# Temporal until root logger is set
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Deck:
    """ The deck of cards from which the user draws """
    EVENT_CARD_TIMEOUT = 20

    def __init__(self, all_cards: List[Card]):
        self._event_cards = {card for card in all_cards if card.card_type == "event"}
        self._response_cards = {card.card_id: card for card in all_cards if card.card_type == "response"}
        # Dictionary where keys are Card objects and values are ints representing current timeout
        self._timeout_event_cards = {}
        self._next_card_id = "random"

    def get_card(self, game_state_handler: GameStateHandler) -> Card:
        if self._next_card_id != "random":
            self._reduce_timeouts()
            return self._response_cards[self._next_card_id]

        possible_event_cards = self._event_cards - self._timeout_event_cards.keys()
        valid_event_cards = {card for card in possible_event_cards if card.is_valid(game_state_handler)}
        if len(valid_event_cards) > 0:
            card = random.choice(tuple(valid_event_cards))
        else:
            # Choose card from smallest timeout
            card = min(self._timeout_event_cards, key=self._timeout_event_cards.get)
            logger.info(f"No more cards to draw - drawing from timed out cards. "
                        f"Drawn card {card}")
            del self._timeout_event_cards[card]

        self._add_card_to_timeout(card)
        self._reduce_timeouts()
        return card

    def set_next_response_card(self, card_id: Union[str, None]):
        self._next_card_id = card_id

    def _add_card_to_timeout(self, event_card: Card):
        """
        Add card to timeout. This means that the card cannot be drawn again for certain
        amount of turns.
        :param event_card: Card to add to timeout
        """
        self._timeout_event_cards[event_card] = Deck.EVENT_CARD_TIMEOUT

    def _reduce_timeouts(self):
        for event_card in self._timeout_event_cards:
            self._timeout_event_cards[event_card] -= 1
            if self._timeout_event_cards[event_card] <= 0:
                del self._timeout_event_cards[event_card]


class Game:
    """Stores state about the current game"""

    def __init__(self, all_cards: List[Card], game_states: dict):
        self.game_state_handler = GameStateHandler(game_states)
        self.deck = Deck(all_cards)

    def take_turn(self):
        card = self.deck.get_card(self.game_state_handler)
        self.game_state_handler.increase_turn()
        logger.debug(f"Drawn card: {card}")
        logger.info(f"Card text: {card.text}")
        logger.debug(f"Game state: {self.game_state_handler}")
        option = input(f"Which option?\n"
                       f"{card.options}\nInput:")
        selected_option = card.options[0] if option == "1" else card.options[1]
        outcome = selected_option.get_outcome()
        logger.debug(f"Outcome of option: {outcome}")
        self.game_state_handler.update_state(outcome.effects)
        self.deck.set_next_response_card(outcome.next_card)
        return card


if __name__ == "__main__":
    with open("data/caveman_game_cards.json") as f:
        _cards = [Card(**card_dict) for card_dict in json.load(f)]
    with open("data/caveman_game_states.json") as f:
        _game_states = json.load(f)
    game = Game(_cards, _game_states)
    for _ in range(10):
        game.take_turn()
