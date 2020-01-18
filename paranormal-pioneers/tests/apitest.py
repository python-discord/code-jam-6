import unittest
import shutil
from project.core import *

class ApiTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_something(self):
        self.assertEqual(True, False)

    def tearDown(self) -> None:
        shutil.rmtree('./.test_fs')


if __name__ == '__main__':
    unittest.main()
