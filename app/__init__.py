from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource

db = SQLAlchemy()
api = Api(title="The Garrison API",
            version='0.1',
            description='The backend API to interface with The Garrison.')

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from app.api_endpoints import about_namespace
    api.add_namespace(about_namespace)

    api.init_app(app)
    return app
