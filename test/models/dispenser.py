from test import TestCase
from app.models import Dispenser, Ingredient

class TestDispenserCreation(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)

    def test_no_exceptions(self):
        d = Dispenser.from_params(0, self.ingredient, 1000)

    def test_ingredient_relation(self):
        d = Dispenser.from_params(0, self.ingredient, 1000)

        self.assertEqual(d.ingredient, self.ingredient)
        self.assertEqual(self.ingredient.dispenser, d)

    def test_change_ingredient(self):
        d = Dispenser.from_params(0, self.ingredient, 1000)
        i = Ingredient.from_params('juice', alcoholic=False)

        d.change_ingredient(i, 500)

        self.assertEqual(d.ingredient, i)
        self.assertEqual(i.dispenser, d)
        self.assertEqual(d.volume, 500)


class TestDispenserVolume(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.dispenser = Dispenser.from_params(0, self.ingredient, 1000)

    def test_has(self):
        self.assertTrue(self.dispenser.has(900))
        self.assertTrue(self.dispenser.has(1000))
        self.assertFalse(self.dispenser.has(1001))
        self.assertRaises(Exception, lambda : self.dispenser.has(-1))

    def test_has_used(self):
        self.assertEqual(self.dispenser.has_used(100), 900)
        self.assertRaises(Exception, lambda : self.dispenser.has_used(-1))


class TestDispenserDispense(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.dispenser = Dispenser.from_params(0, self.ingredient, 1000)

    def test_pass_in_function(self):
        d2 = Dispenser.from_params(2, self.ingredient, 1000, disabled=False)

        self.assertEqual(d2.dispense(100), 100)
        self.assertEqual(d2.volume, 900)


class TestDispenserIndex(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.dispenser1 = Dispenser.from_params(1, self.ingredient, 1000)
        self.dispenser2 = Dispenser.from_params(2, self.ingredient, 1000)

    def test_swap_location(self):
        Dispenser.swap_dispenser_location(self.dispenser1, self.dispenser2)

        self.assertEqual(self.dispenser1.index, 2)
        self.assertEqual(self.dispenser2.index, 1)

    def test_swap_location_with_self(self):
        Dispenser.swap_dispenser_location(self.dispenser1, self.dispenser1)
