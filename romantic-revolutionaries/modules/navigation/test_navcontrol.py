"""Unit Test For NavControl.

   Run these tests with either with "pytest" or python -m "unittest"
   from within the same directory.
"""

import unittest

from modules.navigation.navcont import NavControl, Directions


# This observer is purely to retrieve callbacks for testing
class Observer:
    def __init__(self):
        self.direction = None
        self.distance = None

    def callback(self, direction, distance):
        self.direction = direction
        self.distance = distance


class TestNavControl(unittest.TestCase):
    def setUp(self):
        self.observer = Observer()
        self.nav_control = NavControl()

        self.nav_control.subscribe(self.observer.callback)

    def test_defaults(self):
        self.nav_control.go()

        self.assertEqual(self.observer.direction, Directions.NORTH)
        self.assertEqual(self.observer.distance, 1)

    def test_repeat_distance(self):
        self.nav_control.go(Directions.SOUTH, 5)

        self.assertEqual(self.observer.direction, Directions.SOUTH)
        self.assertEqual(self.observer.distance, 5)

        self.nav_control.go(Directions.NORTH)

        self.assertEqual(self.observer.direction, Directions.NORTH)
        self.assertEqual(self.observer.distance, 5)

    def test_repeat_direction(self):
        self.nav_control.go(Directions.SOUTH, 5)

        self.assertEqual(self.observer.direction, Directions.SOUTH)
        self.assertEqual(self.observer.distance, 5)

        self.nav_control.go(distance=100)

        self.assertEqual(self.observer.direction, Directions.SOUTH)
        self.assertEqual(self.observer.distance, 100)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            self.nav_control.go(direction="bruh")

    def test_invalid_distance(self):
        with self.assertRaises(ValueError):
            self.nav_control.go(distance=0)
