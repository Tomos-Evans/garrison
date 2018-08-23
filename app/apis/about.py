from flask_restplus import Resource, Namespace
from flask import current_app

ns = Namespace('about', description="General information about the Garrison")

@ns.route('/')
class About(Resource):
    def get(self):
        return {
            'version': current_app.config['API_VERSION'],
            'source': 'https://github.com/tomos-evans/garrison',
        }
