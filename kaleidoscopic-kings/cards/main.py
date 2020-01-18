import json
from typing import List


class Option:
    """Basic class to represent an option, and eventually to choose an outcome"""

    def __init__(self, text=None, outcomes=None):
        self.text = text
        self.outcomes = outcomes


class Card:
    """Represents a card to be presented to the user"""

    def __init__(
        self,
        text: str = None,
        card_id: str = None,
        card_type: str = None,
        options=List[Option],
    ):
        self.text = text
        self.card_id = card_id
        self.type = card_type
        self.options = options if len(options) > 0 else None

    def __repr__(self):
        return (
            f"card: \n\ttype: {self.type} \n\tid: {self.card_id} \n\ttext: {self.text}"
        )


def card_from_dict(card_dict: dict) -> Card:
    """Load a card object from a loaded json"""
    options = [Option(**option) for option in card_dict["options"]]
    del card_dict["options"]
    return Card(**card_dict, options=options)


if __name__ == "__main__":
    with open("TestCards.json") as f:
        c = json.load(f)[1]
        card = card_from_dict(c)
        print(card)
