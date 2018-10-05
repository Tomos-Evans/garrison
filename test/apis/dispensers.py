from test.apis import ApiTestCase
from app.models.drinks import Ingredient, Dispenser

class TestDispenser(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.i1 = Ingredient.from_params('vodka', True, 40)
        self.i2 = Ingredient.from_params('gin', True, 35)
        self.d1 = Dispenser.from_params(0,self.i1, 1000)
        self.d2 = Dispenser.from_params(1,self.i2, 500)

    def test_get_all(self):
        response = self.client.get('/api/dispensers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['dispensers']), 2)

    def test_get_one(self):
        response = self.client.get('/api/dispensers/'+str(self.d1.index))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.i1.ref in response.json['ingredient'])

        response = self.client.get('/api/dispensers/-1')
        self.assertEqual(response.status_code, 404)

class TestDispenserPut(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.i1_ref = Ingredient.from_params('vodka', True, 40).ref
        self.i2 = Ingredient.from_params('gin', True, 35)
        self.d1 = Dispenser.from_params(0,type='empty')
        self.d2 = Dispenser.from_params(1,self.i2, 5000, type='optic', disabled=False, dispense_function=lambda a: a)

    def test_change_to_optic_needs_ing_and_vol(self):
        response = self.client.put('/api/dispensers/0', json={
            'type':'optic'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/dispensers/0', json={
            'type':'optic',
            'volume':1000
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/dispensers/0', json={
            'type':'optic',
            'ingredient':self.i1_ref
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/dispensers/0', json={
            'type':'optic',
            'ingredient':self.i1_ref,
            'volume': 200
        })
        self.assertEqual(response.status_code, 200)

    def test_invalid_type(self):
        response = self.client.put('/api/dispensers/0', json={
            'type':'not valid'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/dispensers/0', json={
            'type':None
        })
        self.assertEqual(response.status_code, 400)

    def test_negative_volume(self):
        response = self.client.put('/api/dispensers/1', json={
            'volume':-100
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/dispensers/1', json={
            'volume':20
        })
        self.assertEqual(response.status_code, 200)
    def test_invalid_ing(self):
        response = self.client.put('/api/dispensers/0', json={
            'type': 'optic',
            'volume':20,
            'ingredient': 'fghjk'
        })
        self.assertEqual(response.status_code, 404)

    def test_invalid_index(self):
        response = self.client.put('/api/dispensers/7890', json={
            'type': 'optic',
            'volume':20,
            'ingredient': 'fghjk'
        })
        self.assertEqual(response.status_code, 404)
