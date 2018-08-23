from config import TestingConfig
import unittest
from app import create_app, constants

class TestCase(unittest.TestCase):

    def setUp(self):
        app = create_app(TestingConfig)
        self.app = app.test_client()

    def tearDown(self):
        pass

from test.mechanical import *
