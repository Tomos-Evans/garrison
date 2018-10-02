from flask_restplus import Resource, Namespace, abort, reqparse
from flask import current_app, jsonify, make_response, url_for, request
from app.models.drinks import Drink, DrinkComponent, Ingredient

ns = Namespace('drinks', description="The Menu")

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', type=str, help='The name of the drink', required=True)
post_parser.add_argument('ingredients', type=list, location='json', help='A list of json objects \{ref: <ingredient ref>, measure: <amount in ml>\}', required=True)

@ns.route('/')
class Drinks(Resource):
    def get(self):
        return {
            'drinks': list(map(lambda d: d.as_json(), Drink.query.all()))
        }

    @ns.doc(parser=post_parser)
    @ns.response(201, 'Created')
    @ns.response(400, 'Bad request')
    @ns.response(409, 'Name conflict')
    def post(self):
        args = request.json
        name = args.get('name')
        ingredients = args.get('ingredients')

        if ingredients is None or name is None:
            return make_response(jsonify(message="Missing arguments"), 400)

        if Drink.query.filter_by(name=name).first():
            abort(409, "Name already in use")

        components = []
        for pair in ingredients:
            ref, measure = pair.get('ref'), pair.get('measure')

            if measure is None or measure <= 0:
                return make_response(jsonify(message="Measures must be positive"), 400)
            elif ref is None:
                return make_response(jsonify(message="Must supply ref"), 400)

            i = Ingredient.query.filter_by(ref=ref).first()

            if i:
                components.append(DrinkComponent.from_params(ingredient=i, measure=measure))
            else:
                return make_response(jsonify(message="Invalid ref"), 400)
        if len(components) == 0:
            return make_response(jsonify(message="Drink must contain ingredients"), 400)
        d = Drink.from_params(name, components)
        return make_response(jsonify(href=url_for('drinks_drinks') + d.ref), 201)

@ns.route('/<ref>')
class SingleDrink(Resource):
    @ns.response(200, 'Ok')
    @ns.response(404, 'Not found')
    def get(self, ref):
        d = Drink.query.filter_by(ref=ref).first()
        if d:
            return d.as_json()
        else:
            abort(404, "No ingredient with ref: " + ref)
