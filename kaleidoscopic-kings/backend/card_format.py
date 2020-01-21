from dataclasses import dataclass
import random
from typing import Union, Tuple
import logging

logger = logging.getLogger(__name__)


class GameStateHandler:
    INTEGER_RANGE_INCLUDING = (0, 100)
    FLOAT_RANGE_INCLUDING = (0, 1)

    def __init__(self, game_states: dict):
        self._game_states = game_states
        self._game_turn = 0

    def __repr__(self):
        return str(self._game_states)

    @property
    def game_turn(self):
        return self._game_turn

    def increase_turn(self):
        self._game_turn += 1

    def update_state(self, effects: dict):
        # effects can be None
        if effects is None:
            return

        for key, value in effects.items():
            if type(value) is int:
                self._game_states[key] += value
                self._make_sure_in_range(key, GameStateHandler.INTEGER_RANGE_INCLUDING)
            elif type(value) is float:
                self._game_states[key] += value
                self._make_sure_in_range(key, GameStateHandler.FLOAT_RANGE_INCLUDING)
            elif type(value) is bool:
                self._game_states[key] = value
            else:
                logger.critical(f"Can't update state, unknown state {key}")

    def _make_sure_in_range(self, key: str, value_range: Tuple[int, int]):
        if self._game_states[key] < value_range[0]:
            self._game_states[key] = value_range[0]
        elif self._game_states[key] > value_range[1]:
            self._game_states[key] = value_range[1]

    def check_game_state(self, state_key: str, state_value: Union[int, float, bool]) -> bool:
        try:
            self_key_value = self._game_states[state_key]
        except AttributeError:
            logger.critical(f"Unknown condition {state_key}")
            return False

        if type(state_value) is int:
            return state_value <= self_key_value
        elif type(state_value) is float:
            return state_value * self_key_value <= self_key_value
        elif type(state_value) is bool:
            return state_value == self_key_value
        else:
            logger.warning("Unsupported type passed for check game state.")
            return False


"""
Changing attributes of any of these data classes requires changing json ones too.
Purpose of them is to make sure there is no missing data in json aka it will error if json format
and data class format differ.
"""


@dataclass
class OptionOutcome:
    """
    Represents one of outcomes of a option.
    """
    # Weighted chance for this outcome to happen
    weight: float
    # Next card the player will get if this outcome is chosen. String representing card id.
    # If no specific card is chosen it will be string "random"
    next_card: str
    # Dict of effects that will happen if this outcome is chosen. Keys are state names and values
    # are values to change the state by. For example {"health": -30}
    effects: dict = None


@dataclass
class Option:
    """
    Represents one of 2 options the user is presented for each card.
    """
    text: str
    # List of OptionOutcome objects
    outcomes: list

    def __post_init__(self):
        """
        Initialized outcomes is list of dicts loaded directly from json.
        After init we convert it to list of OptionOutcome objects.
        """
        self.outcomes = [OptionOutcome(**outcome) for outcome in self.outcomes]

    def get_outcome(self) -> OptionOutcome:
        return random.choices(self.outcomes,
                              weights=[outcome.weight for outcome in self.outcomes])[0]


@dataclass()
class Card:
    """Represents a card to be presented to the user."""
    card_id: str
    # Either "event" or "response". Response cards only exist to follow up on event cards.
    card_type: str
    text: str
    # List of Option objects
    options: list
    # Dict of conditions for example {"health": 0.5} and this card would be only valid if player
    # health is more or equal than 50% of it's total value.
    conditions: dict = None

    def __post_init__(self):
        """
        Initialized options is list of dicts loaded directly from json.
        After init we convert it to list of Option objects.
        """
        self.options = [Option(**option) for option in self.options]

    def __hash__(self):
        return hash(self.card_id)

    def is_valid(self, game_state: GameStateHandler):
        if self.conditions is None:
            return True
        else:
            return all(game_state.check_game_state(k, v) for k, v in self.conditions.items())
