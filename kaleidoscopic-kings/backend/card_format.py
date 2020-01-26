import random
import logging
from dataclasses import dataclass
from typing import Union, Tuple, List, Dict, ClassVar

logger = logging.getLogger(__name__)


"""
Changing attributes of any of these data classes requires changing saved json format.
Purpose of them is to make sure there is no missing data in json aka it will error if json format
and data class format differ.

Also they are used for the Editor as they will produce the same output format as given input format.
"""


@dataclass
class GameVariable:
    """
    Can represent game state, condition or effect.

    Currently 3 type of states are supported: int, float and bool.

    The limits for int and float are defined by constants class attributes.
    For example if the _INTEGER_RANGE_INCLUDING is (0, 1000) then that means that states of
    type int, when updated, will never go over 1000 or below 0.
    :raise TypeError, ValueError:
    """
    INTEGER_RANGE_INCLUDING: ClassVar[Tuple[int, int]] = (0, 1000)
    FLOAT_RANGE_INCLUDING: ClassVar[Tuple[float, float]] = (0.0, 1.0)

    state_name_key: str
    value: [int, float, bool]

    def __post_init__(self):
        """Make sure that state is one of the allowed types."""
        if type(self.value) not in (int, float, bool):
            raise TypeError(f"Unknown state type {self.value}.")
        elif (type(self.value) is int and
              not self.INTEGER_RANGE_INCLUDING[0] <= self.value <= self.INTEGER_RANGE_INCLUDING[1]):
            raise ValueError("Int out of range.")
        elif (type(self.value) is float and
              not self.FLOAT_RANGE_INCLUDING[0] <= self.value <= self.FLOAT_RANGE_INCLUDING[1]):
            raise ValueError("Float out of range.")

    def __eq__(self, other_state: "GameVariable"):
        if isinstance(other_state, GameVariable):
            return (isinstance(self.value, type(other_state.value)) and
                    self.value == other_state.value)
        return False

    def __repr__(self):
        return f"{self.state_name_key}:{self.value}"

    def update(self, value: Union[int, float, bool]):
        if type(value) is int:
            self.value += value
            self._make_sure_in_range(self.INTEGER_RANGE_INCLUDING)
        elif type(value) is float:
            self.value += value
            self._make_sure_in_range(self.FLOAT_RANGE_INCLUDING)
        elif type(value) is bool:
            self.value = value
        else:
            logger.critical(f"Can't update state, unknown state type for {value}.")

    def _make_sure_in_range(self, value_range: Union[Tuple[int, int], Tuple[float, float]]):
        min_including, max_including = value_range
        if self.value < min_including:
            self.value = min_including
        elif self.value > max_including:
            self.value = max_including

    def as_dict(self) -> dict:
        """
        Get's the format that is used for saving state/condition/effect in json.
        """
        return {self.state_name_key: self.value}


@dataclass
class MainState(GameVariable):
    """Represents one of the 4 main game states."""
    label: str
    icon_asset: str

    def as_dict(self) -> dict:
        """
        Get's the format that is used for saving main state to json.
        """
        return {self.state_name_key: {self.value, self.label, self.icon_asset}}

    def __repr__(self):
        return str(self.value)


@dataclass
class OptionOutcome:
    """
    Represents one of outcomes of a option.

    weight:      Weighted chance for this outcome to happen.
    next_card:   Next card id the player will get if this outcome is chosen.
                 If no specific card is chosen it will be string "random".
    effects:     Passed as dictionary of effects where keys represent game state to alter
                 and values by how much (as loaded from json). Example {"player_health": -0.3}
                 This is then converted and saved to a list of GameVariable objects.
    """
    weight: float
    next_card: str
    effects: Union[dict, List[GameVariable], None] = None

    def __post_init__(self):
        if self.effects is not None:
            self.effects = [GameVariable(name, value) for name, value in self.effects.items()]


@dataclass
class Option:
    """
    Represents one of options the user is presented for each card.

    text:       Text the player will be presented for this option.
    outcomes:   Passed as dictionary which was loaded from json,
                then it converted and saved as List of OptionOutcome objects.
    """
    text: str
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


class GameState:
    """
    Class that handles state interactions.

    All possible states are passed as dictionary in init. One example of game_states:
    {
     "village_population": 80,
     "world_encountered_dinosaur": false
    }

    Example of main_game_states:
    {
      "player_health": {"value": 1.0, "label": "Health", "icon_asset": "player_health.jpg"},
      ... ,
      ... ,
      "player_something": {"value": 1.0, "label": "Something", "icon_asset": "player_something.jpg"}
    }

    Then these states can easily be called from cards json by using conditions/effects.
    For example card can have key "conditions" with value {"village_population": 50} which will
    make the card valid for the player to draw only if the village_population state is equal or
    higher than 50. Integer and floats are always checked if state is equal or more than condition
    while booleans are just compared.

    Same goes for effects of outcome example outcome has "effects": {"village_population": -10}
    then that outcome will reduce the village_population state by 10.

    There are some special game states that are global no matter the json file and are not limited
    by range. These cannot be modified by card conditions/effects. Currently these are:
    game_turn

    """
    def __init__(self, game_states: dict, main_game_states: Dict[str, Dict]):
        self._main_states_names = tuple(main_game_states.keys())
        self._game_states = self._construct_game_states(game_states, main_game_states)
        self._game_turn = 0

    def __repr__(self):
        return str(self._game_states)

    @classmethod
    def _construct_game_states(cls,
                               game_states: dict,
                               main_game_states
                               ) -> Dict[str, Union[GameVariable, MainState]]:

        if len(main_game_states) != 4:
            raise Exception("4 main states are required.")

        game_states_map = {name: GameVariable(name, value) for name, value in game_states.items()}
        main_game_state_map = {name: MainState(name, **sub_dict) for name, sub_dict in
                               main_game_states.items()}

        if game_states_map.keys() & main_game_state_map.keys():
            raise Exception("One of the main states is already present in "
                            "game states or the other way around.")
        game_states_map.update(main_game_state_map)
        return game_states_map

    def get_main_state(self, state_index: int) -> MainState:
        """
        :param state_index: int 0,1,2 or 3 depending on which MainState you want.
        :return: MainState
        """
        return self._game_states[self._main_states_names[state_index]]

    @property
    def game_turn(self):
        return self._game_turn

    def increase_turn(self):
        self._game_turn += 1

    def update_state(self, effects: List[GameVariable]):
        """
        :param effects: List of GameVariable or None representing changes that modify current game
                        states. If it None nothing is changed.
        :raise: Attribute error is going to be raised if any of the keys in effects is not found in
                game states.
        :raise: TypeError if effect value and it's game state value match are not the same type.
        """
        if effects is None:
            return

        for effect in effects:
            self._make_sure_same_type(effect.value, self._game_states[effect.state_name_key].value)
            self._game_states[effect.state_name_key].update(effect.value)

    @classmethod
    def _make_sure_same_type(cls, variable_1, variable_2):
        if type(variable_1) is not type(variable_2):
            raise TypeError(f"Type value for  {variable_1} and {variable_2} do no match.")

    def _make_sure_in_range(self, key: str,
                            value_range: Union[Tuple[int, int], Tuple[float, float]]):
        min_including, max_including = value_range
        if self._game_states[key] < min_including:
            self._game_states[key] = min_including
        elif self._game_states[key] > max_including:
            self._game_states[key] = max_including

    def check_condition(self, condition: GameVariable) -> bool:
        """
        Check if passed state value is lower or equal to it's current game state value.
        :param condition:
        :return: bool whether the passed state value is lower or equal to it's current
                 game state value. If passed state_key is not found in game states returns False.
        :raise: TypeError if effect value and it's game state value match are not the same type.
        """
        try:
            game_state_value = self._game_states[condition.state_name_key].value
        except KeyError:
            logger.critical(f"Unknown condition {condition}")
            return False

        self._make_sure_same_type(condition.value, game_state_value)

        if type(condition.value) is int:
            return condition.value <= game_state_value
        elif type(condition.value) is float:
            return condition.value <= game_state_value
        elif type(condition.value) is bool:
            return condition.value == game_state_value
        else:
            logger.critical("Unsupported type passed.")
            return False


@dataclass
class Card:
    """Represents a card to be presented to the user.

    card_id:    Unique card name.
    card_type:  Either "event" , "response" or "start".
                Response cards only exist to follow up on event cards.
                There can only be one start card, only difference between event and start card is
                that start card is always drawn first - so you can chain additional response cards
                to it.
    card_image: Image filename including extension.
    text:       Card text.
    options:    Passed as dictionary which was loaded directly from json,
                then it is converted and saved as list of Option objects.
                There can be 0, 1 or 2 options.
    conditions: [optional] Passed as dictionary loaded directly from json example
                {"player_health": 0.5} and this card would only be  valid if player health is more
                or equal than 50%
                After init we convert it to list of GameVariable objects.
    card_sound: [optional] Sound file filename including extension.
    """
    CARD_TYPES: ClassVar[Tuple[str, str]] = ("event", "response", "start")

    card_id: str
    card_type: str
    card_image: str
    text: str
    options: Union[dict, List[Option]]
    conditions: Union[dict, List[GameVariable], None] = None
    card_sound: str = None

    def __post_init__(self):
        self.options = [Option(**option) for option in self.options]
        if self.conditions is not None:
            self.conditions = [GameVariable(name, value) for name, value in self.conditions.items()]
        if self.card_type not in Card.CARD_TYPES:
            raise Exception(f"Invalid card type {self.card_type} for card {self.card_id}")

    def __hash__(self):
        return hash(self.card_id)

    def is_valid(self, game_state: GameState):
        if self.conditions is None:
            return True
        else:
            return all(game_state.check_condition(condition) for condition in self.conditions)
