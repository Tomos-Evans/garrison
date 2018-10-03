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

    # def test_post(self):
    #     response = self.client.post('/api/dispensers/', json={'index':2, 'ingredient':self.i1.ref, 'volume': 100})
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_post_to_existing(self):
    #     response = self.client.post('/api/dispensers/', json={'index':1, 'ingredient':self.i1.ref, 'volume': 100})
    #     self.assertEqual(response.status_code, 409)
    #
    # def test_post_invalid_ing(self):
    #     response = self.client.post('/api/dispensers/', json={'index':2, 'ingredient':'no', 'volume': 100})
    #     self.assertEqual(response.status_code, 404)
