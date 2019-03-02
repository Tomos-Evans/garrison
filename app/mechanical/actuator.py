from statemachine import StateMachine, State, Transition
import time
from app import constants
from app.mechanical.slush_engine import board
from flask import current_app


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

    def press(self):
        if self.current_state.name is not 'lowered':
            self.transition_to('lowered')
        if not current_app.config['TESTING']:
            time.sleep(constants.TIME_TO_WAIT_BETWEEN_PRESSES)
        self.transition_to('raised')
        if not current_app.config['TESTING']:
            time.sleep(constants.TIME_TO_EMPTY_OPTIC)
        self.transition_to('lowered')

    def _raise(self):
        print("Actuator going up")
        board.setIOState(0, self.up_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(constants.ACTUATOR_TRAVEL_TIME)
        board.setIOState(0, self.up_pin, 0)

    def _lower(self):
        print("Actuator going down")
        board.setIOState(0, self.down_pin, 1)
        if not current_app.config['TESTING']:
            time.sleep(constants.ACTUATOR_TRAVEL_TIME)
        board.setIOState(0, self.down_pin, 0)

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
