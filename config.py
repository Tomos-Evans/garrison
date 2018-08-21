import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config():
    # General Flask variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-secret-key'

    # Database variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    FAKE_GPIO=True

class TestingConfig(DevelopmentConfig):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite://'
