import os
from dotenv import load_dotenv

base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

class Config():
    # General Flask variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-secret-key'
    API_VERSION = 0.1

    # Database variables
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mechanical
    FAKE_GPIO = os.environ.get('FAKE_GPIO') in ['1', 'true', 'True']
    if FAKE_GPIO:
        print("Faking GPIO interactions. User FAKE_GPIO=False env var to change.")

class TestingConfig(Config):
    TESTING=True
    FAKE_GPIO=True
    SQLALCHEMY_DATABASE_URI='sqlite://'
