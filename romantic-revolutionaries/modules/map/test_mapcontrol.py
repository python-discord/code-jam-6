"""Test MapControl.

   Run these tests with either with "pytest" or python -m "unittest"
   from within the same directory.
"""


import unittest

from modules.navigation.navcont import NavControl, Directions
from modules.map.MapControl import DungeonMap


# This observer is purely to retrieve callbacks for testing
class Observer:
    def __init__(self):
        self.current_location = None
        self.visible_block = None
        self.did_bonk = False

    def callback(self, current_location, visible_block, did_bonk):
        self.current_location = current_location
        self.visible_block = visible_block
        self.did_bonk = did_bonk
#        print(self.current_location)
#        print(self.did_bonk)
#        for v in visible_block:
#            print(v)


class TestMapControl(unittest.TestCase):
    def setUp(self):
        # setup the initial test map
        DungeonMap.map_vector = [
                [0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]]

        self.observer = Observer()
        self.mc = DungeonMap()
        self.nc = NavControl()

        self.nc.subscribe(self.mc.callback)
        self.mc.subscribe(self.observer.callback)

    def test_bonk(self):
        self.nc.go(Directions.NORTH)
        self.assertEqual(self.observer.did_bonk, True)

        self.nc.go(Directions.WEST)
        self.assertEqual(self.observer.did_bonk, True)

        self.nc.go(Directions.EAST)
        self.assertEqual(self.observer.did_bonk, False)
        self.assertEqual(self.observer.current_location, (1, 2))

        self.nc.go(Directions.WEST)
        self.assertEqual(self.observer.did_bonk, False)

    def test_distance_bonk(self):
        self.nc.go(Directions.NORTH, 10)
        self.assertEqual(self.observer.did_bonk, True)

        self.nc.go(Directions.WEST, 10)
        self.assertEqual(self.observer.did_bonk, True)

        self.nc.go(Directions.EAST, 10)
        self.assertEqual(self.observer.did_bonk, True)
        self.assertEqual(self.observer.current_location, (1, 2))

        self.nc.go(Directions.WEST, 10)
        self.assertEqual(self.observer.did_bonk, True)

    def test_distance_nobonk(self):
        self.nc.unsubscribe(self.mc.callback)
        self.mc.unsubscribe(self.observer.callback)

        DungeonMap.map_vector = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.mc = DungeonMap()
        self.nc.subscribe(self.mc.callback)
        self.mc.subscribe(self.observer.callback)

        self.nc.go(Directions.EAST, 9)
        self.assertEqual(self.observer.did_bonk, False)
        self.assertEqual(self.observer.current_location, (1, 10))

        self.nc.go(Directions.SOUTH, 1)
        self.assertEqual(self.observer.did_bonk, False)
        self.assertEqual(self.observer.current_location, (2, 10))

        self.nc.go(Directions.WEST, 10)
        self.assertEqual(self.observer.did_bonk, True)
        self.assertEqual(self.observer.current_location, (2, 1))
