"""Unit Test For NavControl.

   Run these tests with either with "pytest" or python -m "unittest"
   from within the same directory.
"""


import unittest
import navcont

# This observer is purely to retrieve callbacks for testing
class Observer():
    def __init__(self):
        self.direction = ''
        self.distance=-1

    def callback(self, direction, distance):
        self.direction = direction
        self.distance = distance

class TestNavControl(unittest.TestCase):

    def test_go(self):
        ob = Observer()
        nc = navcont.NavControl()

        nc.subscribe(ob.callback)

        # Test initial defaults
        nc.go()
        self.assertEqual(ob.direction, 'N')
        self.assertEqual(ob.distance, 1)

        # Test lower case call
        nc.go('e', 4)
        self.assertEqual(ob.direction, 'E')
        self.assertEqual(ob.distance, 4)

        # Test repeat previous distance
        nc.go('S')
        self.assertEqual(ob.direction, 'S')
        self.assertEqual(ob.distance, 4)

        # Test repeat previous direction
        nc.go(distance=99)
        self.assertEqual(ob.direction, 'S')
        self.assertEqual(ob.distance, 99)

        # Test upper and lower case directions
        nc.go('N')
        self.assertEqual(ob.direction, 'N')
        nc.go('S')
        self.assertEqual(ob.direction, 'S')
        nc.go('E')
        self.assertEqual(ob.direction, 'E')
        nc.go('W')
        self.assertEqual(ob.direction, 'W')
        nc.go('n')
        self.assertEqual(ob.direction, 'N')
        nc.go('s')
        self.assertEqual(ob.direction, 'S')
        nc.go('e')
        self.assertEqual(ob.direction, 'E')
        nc.go('w')
        self.assertEqual(ob.direction, 'W')

        # Test exception
        self.assertRaises(ValueError, nc.go, 'q')
