from test import TestCase

class TestActuatorTransitions(TestCase):
    def setUp(self):
        super().setUp()
        from app.mechanical.actuator import Actuator
        self.actuator = Actuator()

    def test__initial_idle(self):
        self.assertEqual(self.actuator.current_state.name, 'idle')

    def test_press(self):
        self.actuator.press()
        self.assertEqual(self.actuator.current_state.name, 'lowered')
        self.actuator.press()
        self.assertEqual(self.actuator.current_state.name, 'lowered')
