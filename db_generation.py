from app import db, create_app
from config import DevelopmentConfig
application = create_app(DevelopmentConfig)

with application.app_context():
    db.drop_all()
    db.create_all()
