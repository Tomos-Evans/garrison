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
                    'href': '/api/ingredients/'+Ingredient.query.all()[0].ref,
                    'name': 'vodka',
                    'alcoholic': True,
                    'abs': 40,
                },
                {
                    'href': '/api/ingredients/'+Ingredient.query.all()[1].ref,
                    'name': 'gin',
                    'alcoholic': True,
                    'abs': 35,
                },
                {
                    'href': '/api/ingredients/'+Ingredient.query.all()[2].ref,
                    'name': 'orange juice',
                    'alcoholic': False,
                    'abs': None,
                },
            ]
        }
        self.assertEqual(response.json, target)
