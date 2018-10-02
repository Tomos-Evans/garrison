from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from app import constants

db = SQLAlchemy()

from app import models

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    constants.FAKE_GPIO = app.config['FAKE_GPIO']

    db.init_app(app)

    api = Api(title="The Garrison API",
                version=app.config['API_VERSION'],
                description='The backend API to interface with The Garrison.',
                prefix='/api')

    api.namespaces.pop(0)

    from app.apis.about import ns as about_ns
    api.add_namespace(about_ns)
    from app.apis.ingredients import ns as ingredient_ns
    api.add_namespace(ingredient_ns)

    api.init_app(app)
    return app
