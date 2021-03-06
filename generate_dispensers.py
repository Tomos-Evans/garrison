from app import db, create_app
from config import Config
application = create_app(Config)

from app.models.dispensers import Dispenser

with application.app_context():
    if len(Dispenser.query.all()) == 0:
        for i in range(6):
            d = Dispenser.from_params(i, None, 0, type='optic', dispense_function=lambda : None)
