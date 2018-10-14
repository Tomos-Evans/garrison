from flask_restplus import Resource, Namespace, abort, reqparse, fields, inputs
from flask import current_app, jsonify, make_response, url_for, request

from app.models.dispensers import Dispenser
from app.models.drinks import Ingredient

ns = Namespace('dispensers', description="The dispensers that the garrison has.")

@ns.route('/')
class Dispensers(Resource):
    def get(self):
        ds = Dispenser.query.all()
        return {
            'dispensers': list(map(lambda d: d.as_json(), Dispenser.query.all()))
        }

put_parser = reqparse.RequestParser()
put_parser.add_argument('disable', type=inputs.boolean, help='Disables the dispenser, loosing all state')
put_parser.add_argument('ingredient', type=str, help='The ref of the ingredient that you want to give the dispenser. Ignored if type == "empty"')
put_parser.add_argument('volume', type=str, help='updates the volume of the dispenser. Ignored if type == "empty"')

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

    @ns.doc(parser=put_parser)
    @ns.response(200, 'Success')
    @ns.response(404, 'Not found')
    @ns.response(400, 'Bad request')
    def put(self, index):
        args = put_parser.parse_args()
        ingredient = args.get('ingredient')
        volume = int(args.get('volume')) if args.get('volume') != None else None
        disable = args.get('disable') == True

        d = Dispenser.query.filter_by(index=index).first()
        if d == None:
            abort(404, "No dispenser with index: " + str(index))

        if disable:
            d.disable()
            return make_response(jsonify(d.as_json()), 200)

        if not disable and not d.disabled:
            # The dispenser is already enabled, so only changing volume is alowed
            if ingredient != None:
                i = Ingredient.query.filter_by(ref=ingredient).first()
                if i is None:
                    abort(404, "No ingredient with ref: " + ingredient)
                if volume == None or volume <0:
                    abort(400, "Cannot change ingredient without giving new volume")
                d.change_ingredient(i, volume)
            elif volume != None:
                if volume < 0:
                    abort(400, "Volume cannot be negative")
                d.update_volume(volume)
            return make_response(jsonify(d.as_json()), 200)

        # if type == 'optic' and d.type != 'optic':
        if not disable and d.disabled:
            # The dispensor is disabled, so it needs all info and to update
            # its dispense method
            if ingredient == None or volume == None:
                abort(400, "missing information")

            i = Ingredient.query.filter_by(ref=ingredient).first()
            if i is None:
                abort(404, "No ingredient with ref: " + ingredient)

            if volume < 0:
                abort(400, "Volume must be non negative")

            d.change_ingredient(i, volume)
            d.enable()
            return make_response(jsonify(d.as_json()), 200)
        if not d.disabled and volume != None and volume >=0:
            d.update_volume(volume)
            return make_response(jsonify(d.as_json()), 200)

        return abort(400, "Bad Request")
