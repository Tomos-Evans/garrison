from flask_restplus import Resource, Namespace, abort, fields
from flask import jsonify, make_response, url_for, request
from app.models.drinks import Drink, DrinkComponent, Ingredient

ns = Namespace('drinks', description="The Menu")

ingredient_model = ns.model('IngredientModel', {
    'ref': fields.String(required=True),
    'measure': fields.Integer(min=0),
})

drink_model = ns.model('DrinkModel', {
    'name': fields.String(required=True),
    'ingredients': fields.List(fields.Nested(ingredient_model)),
})


@ns.route('/')
class Drinks(Resource):
    @staticmethod
    def get():
        return {
            'drinks': list(map(lambda d: d.as_json(), Drink.query.all()))
        }

    @ns.expect(drink_model)
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
        return make_response(jsonify(ref=url_for('drinks_drinks') + d.ref), 201)


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
