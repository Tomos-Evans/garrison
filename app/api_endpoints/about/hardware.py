from app.api_endpoints.about import ns
from flask_restplus import Resource

@ns.route('/hardware/trolley')
class Res(Resource):
    @ns.doc("Hardware specs relating to the trolley")
    def get(self):
        return {
            'topSpeed': '0.15m/s',
            'range': '1m',
        }
