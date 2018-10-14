from flask_restplus import Resource, Namespace, abort, reqparse
from flask import current_app, jsonify, make_response, url_for, request
from app.models.drinks import Drink

ns = Namespace('orders', description="Order drinks")

post_parser = reqparse.RequestParser()
post_parser.add_argument('ref', type=str, help='The drink ref', required=True)

@ns.route('/')
class Orders(Resource):
    @ns.doc(parser=post_parser)
    @ns.response(200, 'Success')
    @ns.response(404, 'Drink not found')
    def post(self):
        args = post_parser.parse_args()
        ref = args.get('ref')

        d = Drink.query.filter_by(ref=ref).first()
        if d == None:
            abort(404, "No drink with ref: " + ref)

        # TODO: Make the drink
        return 200
