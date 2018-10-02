from test.apis import ApiTestCase
from app.models.drinks import Ingredient

class TestGet(ApiTestCase):
    def setUp(self):
        super().setUp()
        Ingredient.from_params('vodka', True, 40)
        Ingredient.from_params('gin', True, 35)
        Ingredient.from_params('orange juice', False)

    def test_get_all(self):
        response = self.client.get('/api/ingredients/')
        target = {
            'ingredients': [
                {
                    'location': '/api/ingredients/'+Ingredient.query.all()[0].ref,
                    'ref': Ingredient.query.all()[0].ref,
                    'name': 'vodka',
                    'alcoholic': True,
                    'abs': 40,
                },
                {
                    'location': '/api/ingredients/'+Ingredient.query.all()[1].ref,
                    'ref': Ingredient.query.all()[1].ref,
                    'name': 'gin',
                    'alcoholic': True,
                    'abs': 35,
                },
                {
                    'location': '/api/ingredients/'+Ingredient.query.all()[2].ref,
                    'ref': Ingredient.query.all()[2].ref,
                    'name': 'orange juice',
                    'alcoholic': False,
                    'abs': None,
                },
            ]
        }
        self.assertEqual(response.json, target)

    def test_get_one_that_exists(self):
        ref = Ingredient.query.all()[0].ref
        response = self.client.get('/api/ingredients/'+ref)
        target = {
            'location': '/api/ingredients/'+ref,
            'ref': ref,
            'name': 'vodka',
            'alcoholic': True,
            'abs': 40,
        }
        self.assertEqual(response.json, target)

    def test_one_doesnt_exist(self):
        response = self.client.get('/api/ingredients/not-a-ref')
        self.assertEqual(response.status_code, 404)

    def test_ing_post(self):
        a = {
            'name': 'new ing',
            'alcoholic': True,
            'abs': 12
        }
        b = {
            'name': 'new ing2',
            'alcoholic': False
        }
        response = self.client.post('/api/ingredients/', json=a)
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/api/ingredients/', json=b)
        self.assertEqual(response.status_code, 201)

    def test_abs_requirement(self):
        a = {
            'name': 'new ing',
            'alcoholic': True
        }
        response = self.client.post('/api/ingredients/', json=a)
        self.assertEqual(response.status_code, 400)

    def test_ing_name_confilct(self):
        a = {
            'name': 'vodka',
            'alcoholic': True,
            'abs': 1
        }
        response = self.client.post('/api/ingredients/', json=a)
        self.assertEqual(response.status_code, 409)
