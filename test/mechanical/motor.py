from test import TestCase


class TestMotorMovement(TestCase):

    def setUp(self):
        super().setUp()
        from app.mechanical.slush_engine import motor
        self.motor = motor

    def test_positive(self):
        self.assertEqual(self.motor.move(10), 10)

    def test_negative(self):
        self.assertEqual(self.motor.move(-10), 10)
