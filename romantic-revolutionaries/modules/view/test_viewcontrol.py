"""Unitest the view control.

Run these tests with either with "pytest" or python -m "unittest"
from within the same directory.
"""

import unittest

from modules.view.viewcontrol import ViewControl
from modules.navigation.navcont import NavControl, Directions
from modules.map.MapControl import DungeonMap


class Observer:
    def __init__(self):
        self.descriptive_text = ''

    def callback(self, descriptive_text):
        self.descriptive_text = descriptive_text
        print(self.descriptive_text)


class TestViewControl(unittest.TestCase):
    def setUp(self):
        # setup the initial test map
        DungeonMap.map_vector = [
                [0, 0, 0, 0],
                [0, 1, 6, 0],
                [0, 9, 1, 0],
                [0, 0, 0, 0]]

        self.ob = Observer()
        self.mc = DungeonMap()
        self.nc = NavControl()
        self.vc = ViewControl()

        self.nc.subscribe(self.mc.callback)
        self.mc.subscribe(self.vc.callback)
        self.vc.subscribe(self.ob.callback)

    def test_look(self):
        self.nc.go(Directions.NORTH)
        self.vc.look(Directions.NORTH)
        self.vc.look(Directions.SOUTH)
        self.vc.look(Directions.EAST)
        self.vc.look(Directions.WEST)

