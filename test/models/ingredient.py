from test import TestCase
from app.models import Ingredient

class TestCreation(TestCase):
    def test_alc_needs_abs(self):
        self.assertRaises(Exception, lambda : Ingredient.from_params('Vodka', alcoholic=True))

    def test_not_alc_doesnt_need_abs(self):
        Ingredient.from_params('OJ', alcoholic=False)

class TestRepresentation(TestCase):
    def test_string(self):
        na = Ingredient.from_params('orange juice', alcoholic=False)
        a  = Ingredient.from_params('vodka', alcoholic=True, abs=40)

        self.assertEqual(str(na), "Orange Juice")
        self.assertEqual(str(a),  "Vodka (40%)")

    def test_repr(self):
        a  = Ingredient.from_params('vodka', alcoholic=True, abs=40)
        na = Ingredient.from_params('orange juice', alcoholic=False)

        self.assertEqual(repr(a), "<Ingredient vodka >")
        self.assertEqual(repr(na), "<Ingredient orange juice >")
