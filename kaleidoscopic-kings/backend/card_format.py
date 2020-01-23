import random
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Tuple, List, Type

logger = logging.getLogger(__name__)


class CaveManGame(ABC):
    """
    This class defines game states that should be easily exposed trough GameState object as
    they are more important then the others.
    """
    @property
    @abstractmethod
    def player_health(self):
        ...

    @property
    @abstractmethod
    def player_water(self):
        ...

    @property
    @abstractmethod
    def player_food(self):
        ...


class GameState(CaveManGame):
    """
    Class that handles state interactions.
    Currently 3 type of states are supported: int, float and bool.

    The limits for int and float are defined by constants class attributes.
    For example if the _INTEGER_RANGE_INCLUDING is (0, 1000) then that means that states of
    type int, when updated, will never go over 1000 or below 0.

    All possible states are passed as dictionary in init. One example of such dictionary:
    {
     "village_population": 80,
     "world_encountered_dinosaur": false
    }

    Then these states can easily be called from cards json by using conditions/effects.
    For example card can have key "conditions" with value {"village_population": 50} which will
    make the card valid for the player to draw only if the village_population state is equal or
    higher than 50. Integer and floats are always checked if state is equal or more than condition.

    Same goes for effects for example "effects": {"village_population": -10} will reduce the
    village_population state population by 10.

    There are some special game states that are global no matter the json file and are not limited
    by range. These cannot be modified by card conditions/effects. Currently these are:
    game_turn

    """
    _INTEGER_RANGE_INCLUDING = (0, 1000)
    _FLOAT_RANGE_INCLUDING = (0.0, 1.0)

    def __init__(self, game_states: dict):
        """
        :param game_states: dict of all possible game states with their default state. Example:
                            {
                             "village_population": 80,
                             "world_encountered_dinosaur": false
                            }
        """
        self._game_states = game_states
        self._game_turn = 0

    def __repr__(self):
        return str(self._game_states)

    @property
    def game_turn(self):
        return self._game_turn

    def increase_turn(self):
        self._game_turn += 1

    @property
    def player_health(self):
        return self._game_states["player_health"]

    @property
    def player_water(self):
        return self._game_states["player_water"]

    @property
    def player_food(self):
        return self._game_states["player_food"]

    def update_state(self, effects: dict):
        """
        :param effects: dict or None representing changes that modify current game states. Example:
                        {"village_population": -10}

                        Where key represent name of state to be changed and value is either int,
                        float or bool. The value types have to match between this dict and their
                        state dict representation (self._game_states) for example if
                        village_population state has a int value you can't pass effect
                        {"village_population": 0.5}
        :raise: Attribute error is going to be raised if any of the keys in effects is not found in
                game states.
        :raise: TypeError if effect value and it's game state value match are not the same type.
        """
        if effects is None:
            return

        for state_key, state_value in effects.items():
            if type(state_value) is int:
                self._make_sure_game_state_is_correct_type(state_key, int)
                self._game_states[state_key] += state_value
                self._make_sure_in_range(state_key, self._INTEGER_RANGE_INCLUDING)
            elif type(state_value) is float:
                self._make_sure_game_state_is_correct_type(state_key, float)
                self._game_states[state_key] += state_value
                self._make_sure_in_range(state_key, self._FLOAT_RANGE_INCLUDING)
            elif type(state_value) is bool:
                self._make_sure_game_state_is_correct_type(state_key, bool)
                self._game_states[state_key] = state_value
            else:
                logger.critical(f"Can't update state, unknown state type for {state_key}")

    def _make_sure_game_state_is_correct_type(self,
                                              state_key: str,
                                              _type: Union[Type[int], Type[float], Type[Type[bool]]]
                                              ):
        if type(self._game_states[state_key]) is not _type:
            raise TypeError(f"Type values for effect {state_key} and game state do no match.")

    def _make_sure_in_range(self, key: str,
                            value_range: Union[Tuple[int, int], Tuple[float, float]]):
        min_including, max_including = value_range
        if self._game_states[key] < min_including:
            self._game_states[key] = min_including
        elif self._game_states[key] > max_including:
            self._game_states[key] = max_including

    def check_game_state(self, state_key: str, state_value: Union[int, float, bool]) -> bool:
        """
        Check if passed state value is lower or equal to it's current game state value.
        For example we have loaded these game states and this is their current values:
        {
         "village_population": 80,
         "world_encountered_dinosaur": false
        }

        If we pass "village_population" as state_key and state_value 50 then this will return True.
        :param state_key: state name to check for example "village_population".
        :param state_value: Union[int, float, bool] state value to check
        :return: bool whether the passed state value is lower or equal to it's current
                 game state value. If passed state_key is not found in game states returns False.
        :raise: TypeError if effect value and it's game state value match are not the same type.
        """
        try:
            self_key_value = self._game_states[state_key]
        except AttributeError:
            logger.critical(f"Unknown condition {state_key}")
            return False

        if type(state_value) is int:
            self._make_sure_game_state_is_correct_type(state_key, int)
            return state_value <= self_key_value
        elif type(state_value) is float:
            self._make_sure_game_state_is_correct_type(state_key, float)
            return state_value * self_key_value <= self_key_value
        elif type(state_value) is bool:
            self._make_sure_game_state_is_correct_type(state_key, bool)
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
    # are values to change the state by. For example {"player_health": -30}
    effects: dict = None


@dataclass
class Option:
    """
    Represents one of options the user is presented for each card.
    """
    text: str
    # Passed in init as list of dicts then later saved as list of OptionOutcome objects
    outcomes: List[Union[dict, OptionOutcome]]

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
    # Image filename including extension
    card_image: str
    text: str
    # List of Option objects
    options: Union[dict, List[Option]]
    # Dict of conditions for example {"player_health": 0.5} and this card would only be  valid
    # if player health is more or equal than 50% of it's total value.
    conditions: dict = None
    # Sound file filename including extension
    card_sound: str = None

    def __post_init__(self):
        """
        Initialized options is list of dicts loaded directly from json.
        After init we convert it to list of Option objects.
        """
        self.options = [Option(**option) for option in self.options]

    def __hash__(self):
        return hash(self.card_id)

    def is_valid(self, game_state: GameState):
        if self.conditions is None:
            return True
        else:
            return all(game_state.check_game_state(k, v) for k, v in self.conditions.items())
