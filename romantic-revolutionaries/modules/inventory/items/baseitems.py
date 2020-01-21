from abc import ABC, abstractmethod


class Item(ABC):
    @property
    @abstractmethod
    def characteristic(self):
        pass

    @property
    @abstractmethod
    def asset(self):
        pass


class StackableItem(Item, ABC):
    def __init__(self):
        self._count = 1

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        if count <= 0:
            raise ValueError("Item count can not be set to 0")
        self._count = count

    def __add__(self, other: int):
        self._count += 1

        return self._count

    def __sub__(self, other: int):
        if self._count - 1 > 0:
            self._count -= 1
        else:
            raise ValueError("Item count can not drop below 0")

        return self._count


class NonStackableItem(Item, ABC):
    @property
    def count(self):
        return 1

    def __add__(self, other):
        raise ValueError("Can not add to an un-stackable item")

    def __sub__(self, other):
        raise ValueError("Can not add to an un-stackable item")
