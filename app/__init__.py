from flask import Flask
from flask_restplus import Api
from app import constants

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    constants.FAKE_GPIO = app.config['FAKE_GPIO']

    api = Api(title="The Garrison API",
                version=app.config['API_VERSION'],
                description='The backend API to interface with The Garrison.',
                prefix='/api')

    from app.apis.about import ns as about_ns
    api.add_namespace(about_ns)

    api.init_app(app)
    return app
