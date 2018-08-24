from test import TestCase
from app.models import Dispenser, Ingredient

class TestDispenserCreation(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)

    def test_no_exceptions(self):
        d = Dispenser.from_params('water', self.ingredient, 1000)

    def test_ingredient_relation(self):
        d = Dispenser.from_params('water', self.ingredient, 1000)

        self.assertEqual(d.ingredient, self.ingredient)
        self.assertEqual(self.ingredient.dispenser, d)

    def test_change_ingredient(self):
        d = Dispenser.from_params('water', self.ingredient, 1000)
        i = Ingredient.from_params('juice', alcoholic=False)

        d.change_ingredient(i)

        self.assertEqual(d.ingredient, i)
        self.assertEqual(i.dispenser, d)
