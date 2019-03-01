from app import db, create_app
from config import Config
application = create_app(Config)

with application.app_context():
    db.drop_all()
    db.create_all()
