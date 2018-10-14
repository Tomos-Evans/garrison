from test import TestCase

class ApiTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

from .ingredients import *
from .drinks import *
from .dispensers import *
