from test import TestCase
from app.models import Drink, DrinkComponent, Ingredient

class TestDrinkCreation(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.ingredient2 = Ingredient.from_params('wine', alcoholic=True, abs=5)
        self.drink_component = DrinkComponent.from_params(self.ingredient, 200)
        self.drink_component2 = DrinkComponent.from_params(self.ingredient2, 100)

    def test_creation(self):
        drink = Drink.from_params('drink1', [self.drink_component, self.drink_component2])

        self.assertEqual(drink.components.all(), [self.drink_component, self.drink_component2])

    def test_alcoholic(self):
        alc = Drink.from_params('alc', [self.drink_component, self.drink_component2])
        not_alc = Drink.from_params('not_alc', [self.drink_component])

        self.assertTrue(alc.alcoholic)
        self.assertFalse(not_alc.alcoholic)

class TestOperations(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.ingredient2 = Ingredient.from_params('wine', alcoholic=True, abs=5)
        self.drink_component = DrinkComponent.from_params(self.ingredient, 200)
        self.drink_component2 = DrinkComponent.from_params(self.ingredient2, 100)

    def test_iter(self):
        drink = Drink.from_params('drink1', [self.drink_component, self.drink_component2])

        l = [self.drink_component, self.drink_component2]
        test = [c for c in drink]

        self.assertEqual(l, test)
        self.assertTrue(self.drink_component in drink)

class TestDrinkRepresentation(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)
        self.ingredient2 = Ingredient.from_params('wine', alcoholic=True, abs=5)
        self.drink_component = DrinkComponent.from_params(self.ingredient, 200)
        self.drink_component2 = DrinkComponent.from_params(self.ingredient2, 100)

    def test_string(self):
        drink = Drink.from_params('drink1', [self.drink_component, self.drink_component2])
        self.assertEqual(str(drink), "Drink1")
