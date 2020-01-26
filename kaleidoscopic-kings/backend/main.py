import json
import random
import logging
from typing import List, Dict
from backend import path_handler
from backend.card_format import Card, GameState, OptionOutcome

logger = logging.getLogger(__name__)


class Deck:
    """ The deck of cards from which the user draws """
    EVENT_CARD_TIMEOUT = 20
    EVENT, RESPONSE, START = Card.CARD_TYPES

    def __init__(self, all_cards: List[Card]):
        """
        Handles drawing cards and card responses/time-outs.
        :param all_cards: List of all Card objects that can be used during the game.
        """
        self._event_cards = set()
        self._response_cards = {}
        self._start_card = []
        self._build_deck(all_cards)
        self._next_card_id = "random"
        # Dictionary where keys are Card objects and values are ints representing current timeout
        self._timeout_event_cards = {}

    def _build_deck(self, all_cards: List[Card]):
        for card in all_cards:
            if card.card_type == self.EVENT:
                self._event_cards.add(card)
            elif card.card_type == self.RESPONSE:
                self._response_cards[card.card_id] = card
            elif card.card_type == self.START:
                self._start_card.append(card)

        self._check_valid_deck()

    def _check_valid_deck(self):
        if not self._event_cards:
            raise Exception("No event cards found!")
        elif len(self._start_card) != 1:
            raise Exception("There needs to be exactly 1 start card.")

    def get_card(self, game_state: GameState) -> Card:
        """
        :param game_state: current GameState object. Needed to check current game states with card
                           conditions.
        :return: Card object that is valid based on it's conditions and current game state.
                 When card is drawn it is put
                 If there are no cards left to draw
        """

        # Response cards are set as helper variable. If it isn't random then it's a response card.
        if self._next_card_id != "random":
            self._reduce_timeouts()
            return self._response_cards[self._next_card_id]

        possible_event_cards = self._event_cards - self._timeout_event_cards.keys()
        valid_event_cards = {card for card in possible_event_cards if
                             card.is_valid(game_state)}

        if len(valid_event_cards) > 0:
            card = random.choice(tuple(valid_event_cards))
        else:
            # There are no more cards to choose from the deck as they are either invalid or most
            # of them have already been used and are in time-out.
            # So we choose next card from timed-out cards with the smallest timeout.
            valid_timeout_cards = {card for card in self._timeout_event_cards if
                                   card.is_valid(game_state)}
            card = min(valid_timeout_cards, key=self._timeout_event_cards.get)
            logger.info(f"No more cards to draw - drawing from timed out cards. "
                        f"Drawn card {card}")
            del self._timeout_event_cards[card]

        self._add_card_to_timeout(card)
        self._reduce_timeouts()
        return card

    def get_start_card(self) -> Card:
        return self._start_card[0]

    def set_next_response_card(self, card_id: str):
        self._next_card_id = card_id

    def _add_card_to_timeout(self, event_card: Card):
        """
        Add card to timeout. This means that the card cannot be drawn again for certain
        amount of turns.
        :param event_card: Card to add to timeout.
        """
        self._timeout_event_cards[event_card] = Deck.EVENT_CARD_TIMEOUT

    def _reduce_timeouts(self):
        expired_timeouts = []

        # Reduce it
        for event_card in self._timeout_event_cards:
            self._timeout_event_cards[event_card] -= 1
            if self._timeout_event_cards[event_card] <= 0:
                expired_timeouts.append(event_card)

        # Remove any expired timeouts
        for event_card in expired_timeouts:
            del self._timeout_event_cards[event_card]


class Game:
    """Handles interaction with game states and deck."""

    def __init__(self, all_cards: List[Card], game_states: dict, main_game_state: Dict[str, dict]):
        self._game_state = GameState(game_states, main_game_state)
        self._deck = Deck(all_cards)
        self._game_started = False

    @property
    def game_state(self):
        return self._game_state

    def start_game(self) -> Card:
        """
        First game turn. Always returns "start" card.
        :return: Card of type "start"
        """
        if self._game_started:
            raise Exception("You can't start game that has already been started!")

        self._game_started = True
        return self._draw_card(start_game=True)

    def take_turn(self, previous_card_outcome: OptionOutcome) -> Card:
        """
        :param previous_card_outcome: OptionOutcome from previous card.
        :return: Card
        """
        if not self._game_started:
            raise Exception("Start the game first!")

        self._game_state.update_state(previous_card_outcome.effects)
        self._deck.set_next_response_card(previous_card_outcome.next_card)
        return self._draw_card()

    def _draw_card(self, *, start_game=False) -> Card:
        if start_game:
            card = self._deck.get_start_card()
        else:
            card = self._deck.get_card(self._game_state)
            self._game_state.increase_turn()

        logger.debug(f"Drawn card: {card}")
        logger.info(f"Card text: {card.text}")
        logger.debug(f"Game state: {self._game_state}")
        return card


def load_game(game_story_name: str) -> Game:
    """Loads the backend and returns a game object"""
    with open(path_handler.get_cards_json_path(game_story_name)) as f:
        _cards = [Card(**card_dict) for card_dict in json.load(f)]
    with open(path_handler.get_game_state_json_path(game_story_name)) as f:
        _game_states = json.load(f)
    with open(path_handler.get_global_game_state_json_path(game_story_name)) as f:
        _game_globals = json.load(f)
    return Game(_cards, _game_states, _game_globals["basic_4_states"])
