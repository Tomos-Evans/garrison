from flask_restplus import Namespace

ns = Namespace('about', description="General Garrison information.")

from  app.api_endpoints.about import hardware
