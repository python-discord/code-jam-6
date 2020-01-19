import json
import random
from collections import deque
from typing import List, Optional, Deque


class Option:
    """Basic class to represent an option, and eventually to choose an outcome"""

    def __init__(self, text=None, outcomes=None):
        self.text: str = text
        self.outcome = random.choices(outcomes, weights=[d["weight"] for d in outcomes])[0]
        self.next_card = (
            None if self.outcome["next_card"] == "random" else self.outcome["next_card"]
        )

    def __repr__(self):
        return self.text


class Card:
    """Represents a card to be presented to the user"""

    def __init__(
        self, text: str = None, card_id: str = None, card_type: str = None, options=List[Option],
    ):
        self.text: str = text
        self.card_id: str = card_id
        self.type: str = card_type
        self.option_1: Option = options[0] if len(options) > 0 else None
        self.option_2: Option = options[1] if len(options) > 1 else None

    def __repr__(self):
        return (
            f"card: \n\t"
            f"type: {self.type} \n\t"
            f"id: {self.card_id} \n\t"
            f"text: {self.text} \n\t"
            f"option 1: {self.option_1.text if self.option_1 is not None else None} \n\t"
            f"option 2: {self.option_2.text if self.option_2 is not None else None}\n"
        )


class Deck:
    """The deck of cards from which the user draws"""

    def __init__(self, possible_cards: List[Card]):
        self._queue: Deque = deque()
        self._possible_cards: List[Card] = possible_cards
        self._event_cards: List[Card] = [c for c in possible_cards if c.type == "event"]

        for _ in range(10):
            self.insert_card()

    def get_next_card(self) -> Card:
        """Returns the card which is at the top of the queue, and removes it from the queue"""
        return self._queue.popleft()

    def insert_card(self, card_id: Optional[str] = None):
        """Inserts a card into the queue of upcoming cards. If no id is provided,
        a random card inserted at the back, if an ID is provided,
        then the card with that id is inserted at the front"""
        if card_id is None:
            self._queue.append(random.choice(self._event_cards))
        else:
            card_to_add = next(c for c in self._possible_cards if c.card_id == card_id)
            self._queue.appendleft(card_to_add)


class Game:
    """Stores state about the current game"""

    def __init__(self, possible_cards):
        self.deck = Deck(possible_cards)

    def take_turn(self):
        """A temporary function to take a turn via console input.
        In reality, this kind of interaction would be handled through
        multiple different methods exposed to kivy"""
        card = self.deck.get_next_card()
        print(card)
        print(f"1) {card.option_1}")
        print(f"2) {card.option_2}")
        choice = input("Option 1 or 2? :")
        res = card.option_1 if choice == "1" else card.option_2
        print(res.next_card)
        self.deck.insert_card(res.next_card)


def card_from_dict(card_dict: dict) -> Card:
    """Load a card object from a loaded json"""
    options = [Option(**option) for option in card_dict["options"]]
    del card_dict["options"]
    return Card(**card_dict, options=options)


if __name__ == "__main__":
    with open("TestCards.json") as f:
        cards = [card_from_dict(c) for c in json.load(f)]

    g = Game(cards)
    g.take_turn()
