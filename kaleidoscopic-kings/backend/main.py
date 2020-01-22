import random
from typing import List, Union
import logging
from backend.card_format import Card, GameStateHandler, OptionOutcome

logger = logging.getLogger(__name__)


class Deck:
    """ The deck of cards from which the user draws """
    EVENT_CARD_TIMEOUT = 20

    def __init__(self, all_cards: List[Card]):
        self._event_cards = {card for card in all_cards if card.card_type == "event"}
        self._response_cards = {card.card_id: card for card in all_cards if
                                card.card_type == "response"}
        # Dictionary where keys are Card objects and values are ints representing current timeout
        self._timeout_event_cards = {}
        self._next_card_id = "random"

    def get_card(self, game_state_handler: GameStateHandler) -> Card:
        if self._next_card_id != "random":
            self._reduce_timeouts()
            return self._response_cards[self._next_card_id]

        possible_event_cards = self._event_cards - self._timeout_event_cards.keys()
        valid_event_cards = {card for card in possible_event_cards if
                             card.is_valid(game_state_handler)}
        if len(valid_event_cards) > 0:
            card = random.choice(tuple(valid_event_cards))
        else:
            # Choose card from smallest timeout
            valid_timeout_cards = {card for card in self._timeout_event_cards if
                                   card.is_valid(game_state_handler)}
            card = min(valid_timeout_cards, key=self._timeout_event_cards.get)
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
    """Handles interaction with the saved states and deck."""

    def __init__(self, all_cards: List[Card], game_states: dict):
        self.game_state_handler = GameStateHandler(game_states)
        self.deck = Deck(all_cards)

    def start_game(self) -> Card:
        return self._draw_card()

    def take_turn(self, previous_card_outcome: OptionOutcome) -> Card:
        """
        :param previous_card_outcome: OptionOutcome from previous card.
        :return: Card
        """
        self.game_state_handler.update_state(previous_card_outcome.effects)
        self.deck.set_next_response_card(previous_card_outcome.next_card)
        return self._draw_card()

    def _draw_card(self) -> Card:
        card = self.deck.get_card(self.game_state_handler)
        self.game_state_handler.increase_turn()
        logger.debug(f"Drawn card: {card}")
        logger.info(f"Card text: {card.text}")
        logger.debug(f"Game state: {self.game_state_handler}")
        return card
