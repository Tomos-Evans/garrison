import json
from flask_restplus import Resource, Namespace, abort
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

@ns.route('/<ref>')
class SingleIngredient(Resource):
    def get(self, ref):
        i = Ingredient.query.filter_by(ref=ref).first()
        if i:
            return i.as_json()
        else:
            abort(404, "No ingredient with ref: " + ref)
