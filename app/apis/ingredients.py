import json
from flask_restplus import Resource, Namespace
from flask import current_app

from app.models.drinks import Ingredient

ns = Namespace('ingredients', description="The ingredients that the garrison has.")

@ns.route('/')
class Ingredients(Resource):
    def get(self):
        return {
            'ingredients': list(map(lambda i: i.as_json(), Ingredient.query.all()))
        }

    def post(self):
        pass
