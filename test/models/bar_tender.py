from test import TestCase
from app.bar_tender import BTException, BTBusy, BTCannotCompleteOrder, BarTender
from app.models import Ingredient, Drink, DrinkComponent, Dispenser


class TestBarTender(TestCase):
    def setUp(self):
        super().setUp()
        self.bar_tender = BarTender()

    def test_is_busy_transistions(self):
        self.assertFalse(self.bar_tender.is_busy)
        self.bar_tender.transition_to('busy')
        self.assertTrue(self.bar_tender.is_busy)
        self.bar_tender.transition_to('waiting')
        self.assertFalse(self.bar_tender.is_busy)

    def test_after_make_state(self):
        self.assertFalse(self.bar_tender.is_busy)
        ingredient = Ingredient.from_params('water', alcoholic=False)
        d = Dispenser.from_params(0, ingredient, 1000)
        d.enable()
        component = DrinkComponent.from_params(ingredient, 200)
        drink = Drink.from_params('test', [component])
        self.bar_tender.make(drink)
        self.assertFalse(self.bar_tender.is_busy)

    def test_cant_make_when_disabled(self):
        ingredient = Ingredient.from_params('water', alcoholic=False)
        d = Dispenser.from_params(0, ingredient, 1000)
        component = DrinkComponent.from_params(ingredient, 200)
        drink = Drink.from_params('test', [component])
        self.assertFalse(self.bar_tender.can_make(drink))

    def test_can_make(self):
        ingredient = Ingredient.from_params('water', alcoholic=False)
        d = Dispenser.from_params(0, ingredient, 1000)
        d.enable()
        component = DrinkComponent.from_params(ingredient, 200)
        drink = Drink.from_params('test', [component])
        self.assertTrue(self.bar_tender.can_make(drink))

    def test_cant_make_not_enough_in_dispenser(self):
        ingredient = Ingredient.from_params('water', alcoholic=False)
        Dispenser.from_params(0, ingredient, 100)
        component = DrinkComponent.from_params(ingredient, 200)
        drink = Drink.from_params('test', [component])
        self.assertFalse(self.bar_tender.can_make(drink))

    def test_cant_make_no_dispenser_with_ingredient(self):
        ingredient = Ingredient.from_params('water', alcoholic=False)
        component = DrinkComponent.from_params(ingredient, 200)
        drink = Drink.from_params('test', [component])
        self.assertFalse(self.bar_tender.can_make(drink))


class TestBTException(TestCase):
    def test_bt_exception_json(self):
        for exception in [BTException, BTCannotCompleteOrder, BTBusy]:
            try:
                raise exception('my message')
            except BTException as e:
                self.assertEqual(e.message, 'my message')
                self.assertEqual(e.as_json(), {
                    'error': 'bar tender exception',
                    'message': 'my message',
                })
