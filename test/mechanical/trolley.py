from test import TestCase
from app.constants import HOME_POS, MAX_RIGHT

class TestTrolleyMovement(TestCase):
    def setUp(self):
        super().setUp()
        from app.mechanical.trolley import Trolley
        from app.mechanical.stepper import Stepper
        self.trolley = Trolley(stepper=Stepper())

    def test_within_bounds(self):
        self.assertEqual(self.trolley.move_to(10), 10)
        self.assertEqual(self.trolley.current_pos, 10)

    def test_go_home(self):
        self.assertEqual(self.trolley.go_home(), HOME_POS)
        self.assertEqual(self.trolley.current_pos, HOME_POS)


    def test_move_left_too_far(self):
        self.assertEqual(self.trolley.move_to(-100), 0)
        self.assertEqual(self.trolley.current_pos, 0)

    def test_move_right_too_far(self):
        self.assertEqual(self.trolley.move_to(MAX_RIGHT+1), MAX_RIGHT)
        self.assertEqual(self.trolley.current_pos, MAX_RIGHT)

    def test_multiple_moves(self):
        self.assertEqual(self.trolley.go_home(), HOME_POS)
        self.assertEqual(self.trolley.move_to(MAX_RIGHT+1), MAX_RIGHT)
        self.assertEqual(self.trolley.move_to(10), 10)
        self.assertEqual(self.trolley.go_home(), HOME_POS)
