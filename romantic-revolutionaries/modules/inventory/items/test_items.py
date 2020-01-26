import unittest

from modules.inventory.items.baseitems import StackableItem, NonStackableItem

characteristic = "An Example of a stackable item!"
asset = "path/to/asset"


class ExampleStackable(StackableItem):
    @property
    def characteristic(self):
        return characteristic

    @property
    def asset(self):
        return asset


class ExampleNonStackable(NonStackableItem):
    @property
    def characteristic(self):
        return characteristic

    @property
    def asset(self):
        return asset


class TestStackableItems(unittest.TestCase):
    def setUp(self):
        self.item = ExampleStackable()

    def test_item_defaults(self):
        self.assertEqual(self.item.count, 1)
        self.assertEqual(self.item.characteristic, characteristic)
        self.assertEqual(self.item.asset, asset)

    def test_add_item(self):
        self.item + 1
        self.assertEqual(self.item.count, 2, msg="Add one item")

        self.item + 10
        self.assertEqual(self.item.count, 12, msg="Add multiple items")

    def test_subtract_item(self):
        self.item.count = 4
        self.item - 1
        self.assertEqual(self.item.count, 3, msg="Subtract 1 item")

        self.item - 2
        self.assertEqual(self.item.count, 1, msg="Subtract multiple items")

    def test_negative_subtract(self):
        with self.assertRaises(ValueError):
            self.item - 1

        self.assertEqual(self.item.count, 1)

    def test_assign_count(self):
        self.item.count = 100

        self.assertEqual(self.item.count, 100)
        self.item.count = 1

    def test_negative_assign(self):
        with self.assertRaises(ValueError):
            self.item.count = 0

        with self.assertRaises(ValueError):
            self.item.count = -100

        self.assertEqual(self.item.count, 1)


class TestNonStackableItem(unittest.TestCase):
    def setUp(self):
        self.item = ExampleNonStackable()

    def test_item_defaults(self):
        self.assertEqual(self.item.count, 1)
        self.assertEqual(self.item.characteristic, characteristic)
        self.assertEqual(self.item.asset, asset)

    def test_add_item(self):
        with self.assertRaises(ValueError):
            self.item + 1

    def test_subtract_item(self):
        with self.assertRaises(ValueError):
            self.item - 1


if __name__ == '__main__':
    item_suite = unittest.TestSuite()
    item_suite.addTest(TestNonStackableItem())
    item_suite.addTest(TestStackableItems())

    runner = unittest.TextTestRunner()
    runner.run(item_suite)
