from flask import Flask
from flask.logging import default_handler
import logging
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app import constants

logger = logging.getLogger('logger')
logger.setLevel('DEBUG')
logger.addHandler(default_handler)

db = SQLAlchemy()
migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.logger.info("Creating new application")
    CORS(app, resources={r"/api/*": {'origins': '*'}})
    app.config.from_object(config)
    constants.FAKE_GPIO = app.config['FAKE_GPIO']

    app.logger.info(f"FAKE_GPIO: {app.config['FAKE_GPIO']}")
    app.logger.info(f"Garrison version: {app.config['API_VERSION']}")
    app.logger.info(f"Attempting to use db at: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(title="The Garrison API",
              version=app.config['API_VERSION'],
              description='The backend API to interface with The Garrison.',
              prefix='/api',
              doc='/docs/api')

    api.namespaces.pop(0)

    from app.apis.about import ns as about_ns
    api.add_namespace(about_ns)
    from app.apis.ingredients import ns as ingredient_ns
    api.add_namespace(ingredient_ns)
    from app.apis.drinks import ns as drinks_ns
    api.add_namespace(drinks_ns)
    from app.apis.dispensers import ns as dispensers_ns
    api.add_namespace(dispensers_ns)
    from app.apis.orders import ns as orders_ns
    api.add_namespace(orders_ns)

    api.init_app(app)

    from app.bar_tender import BarTender
    app.bar_tender = BarTender()

    return app
