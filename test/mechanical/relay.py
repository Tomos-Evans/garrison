from test import TestCase

class TestRelay(TestCase):
    def setUp(self):
        super().setUp()
        from app.mechanical.relay import Relay
        self.relay = Relay(pin_number=10)

    def test_starting_state(self):
        self.assertEqual(self.relay.current_state.name, 'low')

    def test_off_to_on(self):
        a = self.relay.current_state.name
        self.relay.change_high()
        b = self.relay.current_state.name
        self.relay.change_high()
        c = self.relay.current_state.name
        self.relay.change_low()
        d = self.relay.current_state.name
        self.relay.change_low()
        e = self.relay.current_state.name
        self.relay.change_high()
        f = self.relay.current_state.name

        self.assertEqual(a, 'low')
        self.assertEqual(b, 'high')
        self.assertEqual(c, 'high')
        self.assertEqual(d, 'low')
        self.assertEqual(f, 'high')
