from statemachine import StateMachine, State, Transition
import time
from app import constants, logger
from app.mechanical.slush_engine import board
from flask import current_app
from app.logging_helpers import wrap_in_logs


class Actuator(StateMachine):
    def __init__(self, up_pin=constants.ACTUATOR_UP_PIN, down_pin=constants.ACTUATOR_DOWN_PIN):
        super().__init__()
        self.add(State('raised'))
        self.add(State('lowered'))
        self.add(State('idle', is_starting_state=True, will_exit=self._localise))
        self.add(Transition('idle', ['lowered']))
        self.add(Transition('lowered', ['raised'], before=self._raise))
        self.add(Transition('raised', ['lowered'], before=self._lower))

        self.up_pin = up_pin
        self.down_pin = down_pin

    @wrap_in_logs("Pressing Actuator", "Pressed")
    def press(self):
        if self.current_state.name is not 'lowered':
            self.transition_to('lowered')
        if not current_app.config['TESTING']:
            time.sleep(constants.TIME_TO_WAIT_BETWEEN_PRESSES)
        self.transition_to('raised')
        if not current_app.config['TESTING']:
            time.sleep(constants.TIME_TO_EMPTY_OPTIC)
        self.transition_to('lowered')

    @wrap_in_logs("Raising Actuator", "Raised")
    def _raise(self):
        board.setIOState(0, self.up_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(constants.ACTUATOR_TRAVEL_TIME)
        board.setIOState(0, self.up_pin, 0)

    @wrap_in_logs("Lowering Actuator", "Lowered")
    def _lower(self):
        board.setIOState(0, self.down_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(constants.ACTUATOR_TRAVEL_TIME)
        board.setIOState(0, self.down_pin, 0)

    @wrap_in_logs("Localising Actuator", "Actuator is Localised")
    def _localise(self):
        board.setIOState(0, self.down_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(6)
        board.setIOState(0, self.down_pin, 0)

        board.setIOState(0, self.up_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(2.5)
        board.setIOState(0, self.up_pin, 0)


actuator = Actuator()
