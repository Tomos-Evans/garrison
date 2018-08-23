from test import TestCase
from app.models import Ingredient

class TestIngredientCreation(TestCase):
    def test_alc_needs_abs(self):
        self.assertRaises(Exception, lambda : Ingredient.from_params('Vodka', alcoholic=True))

    def test_not_alc_doesnt_need_abs(self):
        Ingredient.from_params('OJ', alcoholic=False)

class TestIngredientRepresentation(TestCase):
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

class TestIngredientOperations(TestCase):
    def test_equality(self):
        a  = Ingredient.from_params('vodka', alcoholic=True, abs=40)
        b  = Ingredient.from_params('vodka1', alcoholic=True, abs=40)
        c  = Ingredient.from_params('vodka2', alcoholic=False)

        self.assertEqual(a, a)
        self.assertNotEqual(a,b)
        self.assertNotEqual(a,c)
