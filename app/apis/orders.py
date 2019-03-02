from flask_restplus import Resource, Namespace, abort, reqparse
from app.models.drinks import Drink
from flask_cors import cross_origin
from flask import current_app, make_response, jsonify
from app.bar_tender import BTException

ns = Namespace('orders', description="Order drinks")

post_parser = reqparse.RequestParser()
post_parser.add_argument('ref', type=str, help='The drink ref', required=True)


@ns.route('/')
class Orders(Resource):
    @ns.doc(parser=post_parser)
    @ns.response(200, 'Success')
    @ns.response(404, 'Drink not found')
    @cross_origin()
    def post(self):
        args = post_parser.parse_args()
        ref = args.get('ref')

        d = Drink.query.filter_by(ref=ref).first()
        if d is None:
            abort(404, "No drink with ref: " + ref)

        try:
            current_app.bar_tender.make(d)
            return make_response(jsonify({
                       'message': 'order complete',
                   }), 200)
        except BTException as e:
            return make_response(jsonify(e.as_json()), 400)
