from test.apis import ApiTestCase
from app.models.drinks import Ingredient, DrinkComponent, Drink

class TestDrink(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.i1 = Ingredient.from_params('vodka', True, 40).ref
        self.i2 = Ingredient.from_params('gin', True, 35).ref
        self.i3 = Ingredient.from_params('orange juice', False).ref

    def test_drink_post(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1, 'measure': 10}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 201)

    def test_drink_name_clash(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1, 'measure': 10}, {'ref': self.i2, 'measure': 20}]})
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1, 'measure': 10}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 409)

    def test_drink_missing_measure(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 400)

    def test_drink_missing_ing(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'measure': 20}]})
        self.assertEqual(response.status_code, 400)

    def test_drink_no_components(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': []})
        self.assertEqual(response.status_code, 400)

    def test_drink_measure_negative(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref': self.i1, 'measure': 0}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 400)

    def test_drink_bad_ing_ref(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1', 'ingredients': [{'ref':'fgh', 'measure': 0}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 400)

    def test_drink_missing_args(self):
        response = self.client.post('/api/drinks/', json={'name': 'd1'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/api/drinks/', json={'ingredients': [{'ref':'fgh', 'measure': 0}, {'ref': self.i2, 'measure': 20}]})
        self.assertEqual(response.status_code, 400)

    def test_get_drinks(self):
        d = Drink.from_params(name="hi", components=[DrinkComponent.from_params(ingredient = Ingredient.from_params('orange', False), measure=20)])
        response = self.client.get('/api/drinks/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['drinks'][0]['ref'] == d.ref)

    def test_get_single_drink(self):
        d = Drink.from_params(name="hi", components=[DrinkComponent.from_params(ingredient = Ingredient.from_params('orange', False), measure=20)])
        response = self.client.get('/api/drinks/'+d.ref)
        self.assertEqual(response.json['ref'], d.ref)
        response = self.client.get('/api/drinks/ghnj')
        self.assertEqual(response.status_code,  404)
