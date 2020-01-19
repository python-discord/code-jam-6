from queue import Queue, Empty
from typing import Iterable, Optional, Dict

from project.core._core.apibase import ApiBase
from project.core._core.vm import OSApiException


class Event:
    pass


class EventApi(ApiBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._evqs: Dict[str, Queue[Event]] = {}

    def raise_event(self, ev: Event, usrs: Iterable[str]) -> None:
        """raise an event for the terminals in usrs"""
        for usr in usrs:
            try:
                self._evqs[usr].put(ev,block=False)
            except KeyError:
                raise OSApiException(f"No such terminal '{usr}'")

    def get_event(self, usr: str) -> Optional[Event]:
        """if there is an event for the given handler, return it, else return None"""
        try:
            return self._evqs[usr].get(block=False)
        except KeyError:
            raise OSApiException(f"No such terminal '{usr}'")
        except Empty:
            return None

    def add_event_handler(self, usr: str):
        self._evqs[usr] = Queue()




