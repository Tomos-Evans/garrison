import json
from flask_restplus import Resource, Namespace, abort, reqparse, fields, inputs
from flask import current_app, jsonify, make_response, url_for

from app.models.drinks import Ingredient

ns = Namespace('ingredients', description="The ingredients that the garrison has.")

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, help='The name of the ingredient', required=True)
post_parser.add_argument('alcoholic', type=inputs.boolean, help='Is the ingredient alcoholic', required=True)
post_parser.add_argument('abs', type=int, help='The ABS of the ingredient if alcoholic', required=False)

@ns.route('/')
class Ingredients(Resource):
    def get(self):
        return {
            'ingredients': list(map(lambda i: i.as_json(), Ingredient.query.all()))
        }

    @ns.doc(parser=post_parser)
    @ns.response(201, 'Created')
    @ns.response(400, 'Alcoholic drinks must specify ABS')
    @ns.response(409, 'Name conflict')
    def post(self):
        args = post_parser.parse_args()
        name = args['name']
        alcoholic = args['alcoholic']
        abs = args['abs']

        if alcoholic and not abs:
            abort(400, "alcoholic drinks must specify ABS")
        if Ingredient.query.filter_by(name=name).first():
            abort(409, "Name already in use")
        i = Ingredient.from_params(name, alcoholic, abs)
        return make_response(jsonify(location=url_for('ingredients_ingredients') + i.ref, ref=i.ref), 201)

@ns.route('/<ref>')
class SingleIngredient(Resource):
    @ns.response(200, 'Ok')
    @ns.response(404, 'Not found')
    def get(self, ref):
        i = Ingredient.query.filter_by(ref=ref).first()
        if i:
            return i.as_json()
        else:
            abort(404, "No ingredient with ref: " + ref)
