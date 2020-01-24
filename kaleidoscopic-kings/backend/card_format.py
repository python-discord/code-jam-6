import random
import logging
from dataclasses import dataclass
from typing import Union, Tuple, List

logger = logging.getLogger(__name__)


@dataclass
class MainState:
    value: Union[int, float, bool]
    label: str
    icon_asset: str


class MainStatesHandler:
    # TODO check typehint
    def __init__(self, main_four_states):
        if len(main_four_states) != 4:
            raise Exception("4 main states are required.")

        # keys are as they were while values are converted to MainState instead of being dict
        self._mapping = {key: MainState(**sub_dict) for key, sub_dict in main_four_states.items()}

    def is_one_of_main_game_states(self, game_state: str) -> bool:
        return game_state in self._mapping

    def get_state_by_index(self, index: int) -> MainState:
        return tuple(self._mapping.values())[index]

    def get_state_by_key(self, key: str):
        return self._mapping[key]

    def __getitem__(self, key: str) -> MainState:
        return self._mapping[key].value

    def __setitem__(self, key, value):
        self._mapping[key].value = value

    def __iter__(self):
        for main_game_state in self._mapping:
            yield main_game_state

    def __repr__(self):
        return str(self._mapping)


class GameState:
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

    # TODO checkl typehint
    def __init__(self, game_states: dict, main_game_states):
        """
        :param game_states: dict of all possible game states with their default state. Example:
                            {
                             "village_population": 80,
                             "world_encountered_dinosaur": false
                            }
        """
        self._main_game_states = MainStatesHandler(main_game_states)
        self._game_states = game_states
        self._game_turn = 0

    def __repr__(self):
        return f"{self._main_game_states} , {self._game_states}"

    def get_main_state(self, state_index: int) -> MainState:
        """
        :param state_index: int 0,1,2 or 3 depending on which MainState you want.
        :return: MainState
        """
        return self._main_game_states.get_state_by_index(state_index)

    @property
    def game_turn(self):
        return self._game_turn

    def increase_turn(self):
        self._game_turn += 1

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

        for effect_state_key, effect_value in effects.items():
            if self._main_game_states.is_one_of_main_game_states(effect_state_key):
                self._update_game_state(self._main_game_states, effect_state_key, effect_value)
            else:
                self._update_game_state(self._game_states, effect_state_key, effect_value)

    def _update_game_state(self,
                           container_reference: Union[dict, MainStatesHandler],
                           effect_state_key: str,
                           effect_state_value: Union[int, float, bool]):

        self._make_sure_game_states_are_same_type(container_reference[effect_state_key],
                                                  effect_state_value)

        if type(effect_state_value) is int:
            container_reference[effect_state_key] += effect_state_value
            # TODO CHECK
            # self._make_sure_in_range(effect_state_key, self._INTEGER_RANGE_INCLUDING)
        elif type(effect_state_value) is float:
            container_reference[effect_state_key] += effect_state_value
            # self._make_sure_in_range(effect_state_key, self._FLOAT_RANGE_INCLUDING)
        elif type(effect_state_value) is bool:
            container_reference[effect_state_key] = effect_state_value
        else:
            logger.critical(f"Can't update state, "
                            f"unknown state type for {effect_state_key} {effect_state_value}")

    @classmethod
    def _make_sure_game_states_are_same_type(cls, current_game_state, applied_game_state):
        if type(current_game_state) is not type(applied_game_state):
            raise TypeError(f"Type value for applied game state value {applied_game_state} and "
                            f"current game state {current_game_state} do no match.")

    def _make_sure_in_range(self, key: str,
                            value_range: Union[Tuple[int, int], Tuple[float, float]]):
        min_including, max_including = value_range
        if self._game_states[key] < min_including:
            self._game_states[key] = min_including
        elif self._game_states[key] > max_including:
            self._game_states[key] = max_including

    def check_game_state(self,
                         condition_state_key: str,
                         condition_state_value: Union[int, float, bool]) -> bool:
        """
        Check if passed state value is lower or equal to it's current game state value.
        For example we have loaded these game states and this is their current values:
        {
         "village_population": 80,
         "world_encountered_dinosaur": false
        }

        If we pass "village_population" as state_key and state_value 50 then this will return True.
        :param condition_state_key: state name to check for example "village_population".
        :param condition_state_value: Union[int, float, bool] state value to check
        :return: bool whether the passed state value is lower or equal to it's current
                 game state value. If passed state_key is not found in game states returns False.
        :raise: TypeError if effect value and it's game state value match are not the same type.
        """
        try:
            game_state_value = self._main_game_states[condition_state_key]
        except KeyError:
            try:
                game_state_value = self._game_states[condition_state_key]
            except KeyError:
                logger.critical(f"Unknown condition {condition_state_key}")
                return False

        if type(condition_state_value) is int:
            self._make_sure_game_states_are_same_type(game_state_value, condition_state_value)
            return condition_state_value <= game_state_value
        elif type(condition_state_value) is float:
            self._make_sure_game_states_are_same_type(game_state_value, condition_state_value)
            return condition_state_value * game_state_value <= game_state_value
        elif type(condition_state_value) is bool:
            self._make_sure_game_states_are_same_type(game_state_value, condition_state_value)
            return condition_state_value == game_state_value
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
