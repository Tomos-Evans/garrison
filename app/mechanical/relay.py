from app.constants import FAKE_GPIO
from statemachine import StateMachine, State, Transition

class Relay(StateMachine):

    def __init__(self, pin_number):
        super().__init__()
        self.add(State('high'))
        self.add(State('low', is_starting_state=True))
        self.add(Transition('high', ['low'], after=lambda : self._change_low ))
        self.add(Transition('low', ['high'], after=lambda : self._change_high ))

        self.pin_number = pin_number

    def change_high(self):
        if self.can_transition_to('high'):
            self.transition_to('high')

    def change_low(self):
        if self.can_transition_to('low'):
            self.transition_to('low')

    def _change_high(self):
        if FAKE_GPIO:
            pass
        else:
            #TODO: Turn the relay on
            pass

    def _change_low(self):
        if FAKE_GPIO:
            pass
        else:
            #TODO: Turn the relay off
            pass
