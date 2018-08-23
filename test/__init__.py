from config import TestingConfig
import unittest
from app import create_app, db

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

from test.mechanical import *
from test.models import *
