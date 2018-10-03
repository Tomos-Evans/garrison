from flask_restplus import Resource, Namespace, abort, reqparse, fields, inputs
from flask import current_app, jsonify, make_response, url_for

from app.models.dispensers import Dispenser
from app.models.drinks import Ingredient

ns = Namespace('dispensers', description="The dispensers that the garrison has.")

# post_parser = reqparse.RequestParser()
# post_parser.add_argument('index', type=int, help='The index of the dispenser', required=True)
# post_parser.add_argument('volume', type=int, help='The volume remaining in the dispenser', required=False)
# post_parser.add_argument('ingredient', type=str, help='The ingredient ref', required=True)

@ns.route('/')
class Dispensers(Resource):
    def get(self):
        ds  =Dispenser.query.all()
        return {
            'dispensers': list(map(lambda d: d.as_json(), Dispenser.query.all()))
        }

    # @ns.doc(parser=post_parser)
    # @ns.response(201, 'Created')
    # @ns.response(404, 'Ingredient not found')
    # @ns.response(409, 'Index in use')
    # def post(self):
    #     args = post_parser.parse_args()
    #     index = args['index']
    #     volume = args['volume']
    #     ref = args['ingredient']
    #
    #     if Dispenser.query.filter_by(index=index).first():
    #         abort(409, "Index already full, consider PUT to edit existing dispenser")
    #     i = Ingredient.query.filter_by(ref=ref).first()
    #     if i is None:
    #         abort(404, "Ingredient not found")
    #
    #     d = Dispenser.from_params(index, i, volume)
    #     return make_response(jsonify(d.as_json()), 201)

@ns.route('/<index>')
class SingleDispenser(Resource):
    @ns.response(200, 'Ok')
    @ns.response(404, 'Not found')
    def get(self, index):
        d = Dispenser.query.filter_by(index=index).first()
        if d:
            return jsonify(d.as_json())
        else:
            abort(404, "No dispenser with index: " + str(index))
