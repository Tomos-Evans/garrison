from flask_restplus import Resource, Namespace, abort, reqparse, fields, inputs
from flask import current_app, jsonify, make_response, url_for

from app.models.dispensers import Dispenser
from app.models.drinks import Ingredient

ns = Namespace('dispensers', description="The dispensers that the garrison has.")

@ns.route('/')
class Dispensers(Resource):
    def get(self):
        ds  =Dispenser.query.all()
        return {
            'dispensers': list(map(lambda d: d.as_json(), Dispenser.query.all()))
        }

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
