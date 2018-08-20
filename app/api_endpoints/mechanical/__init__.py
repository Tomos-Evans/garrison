from flask_restplus import Namespace,Resource
from app.mechanical import motor

ns = Namespace('mechanical', description="Low level mechanical control")

@ns.route('/slush')
class Res(Resource):
    @ns.doc("Direct slush engine")
    def post(self):
        motor.move(100000000000000000000000)
        return 200
