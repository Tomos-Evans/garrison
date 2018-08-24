from test import TestCase
from app.constants import STEPS_PER_CM
class TestStepperMovement(TestCase):
    def setUp(self):
        super().setUp()
        from app.mechanical.stepper import Stepper
        self.stepper = Stepper()

    def test_move_right(self):
        self.assertEqual(self.stepper.move_right(10), 10*STEPS_PER_CM)

    def test_move_left(self):
        self.assertEqual(self.stepper.move_left(10), -10*STEPS_PER_CM)

    def test_move_relative(self):
        self.assertEqual(self.stepper.move_relative(10), 10*STEPS_PER_CM)
        self.assertEqual(self.stepper.move_relative(-10), -10*STEPS_PER_CM)
