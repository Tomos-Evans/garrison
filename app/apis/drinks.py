from flask_restplus import Resource, Namespace, abort, reqparse
from app.models.drinks import Drink, DrinkComponent

ns = Namespace('drinks', description="The Menu")

@ns.route('/')
class Drinks(Resource):
    def get(self):
        return {
            'drinks': list(map(lambda d: d.as_json(), Drink.query.all()))
        }
