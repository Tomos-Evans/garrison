from test import TestCase
from app.models import DrinkComponent, Ingredient

class TestDrinkComponentCreation(TestCase):
    def setUp(self):
        super().setUp()
        self.ingredient = Ingredient.from_params('water', alcoholic=False)

    def test_creation(self):
        drink_component = DrinkComponent.from_params(self.ingredient, 200)

        self.assertEqual(self.ingredient, drink_component.ingredient)

class TestDrinkComponentRepresentation(TestCase):
    def setUp(self):
        super().setUp()
        ingredient = Ingredient.from_params('water', alcoholic=False)
        self.drink_component = DrinkComponent.from_params(ingredient, 200)

    def test_string(self):
        self.assertEqual(str(self.drink_component), "Water (200ml)")

    def test_repr(self):
        self.assertEqual(repr(self.drink_component), "<DrinkComponent "+str(self.drink_component.ingredient)+" >")
