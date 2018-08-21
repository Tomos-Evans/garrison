from test import TestCase

from app.models import Ingredient

class TestDrink(TestCase):
    def test_equal(self):
        i = Ingredient.from_params('vodka', True, 40)
        self.assertEqual(1,1)
