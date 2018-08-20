from app import create_app
from config import Config, DevelopmentConfig

app = create_app(DevelopmentConfig)
