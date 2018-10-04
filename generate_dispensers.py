from app import db, create_app
from config import DevelopmentConfig
application = create_app(DevelopmentConfig)

from app.models.dispensers import Dispenser

with application.app_context():
    for i in range(6):
        d = Dispenser.from_params(i, None, 0, type='empty', dispense_function=lambda : None)
