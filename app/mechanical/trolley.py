from statemachine import StateMachine, State, Transition
from app.constants import HOME_POS, MAX_RIGHT, LIMIT_SWITCH_STANDOFF
from app import logger
from flask import current_app
from app.logging_helpers import wrap_in_logs


class Trolley(StateMachine):
    def __init__(self, stepper):
        super().__init__()
        self.add(State('idle', will_enter=self.idle, will_exit=self.localise))
        self.add(State('moving'))
        self.add(State('stopped', is_starting_state=True))
        self.add(Transition('idle', ['stopped']))
        self.add(Transition('stopped', ['moving', 'idle']))
        self.add(Transition('moving', ['stopped']))

        self.stepper = stepper
        self.current_pos = None

        self.transition_to('idle')

    @wrap_in_logs("Moving Trolley to home position", "Trolley is at home position")
    def go_home(self):
        r = self.move_to(HOME_POS)
        return r

    @wrap_in_logs("Trolley starting move", "Trolley finished move")
    def move_to(self, pos):
        if self.can_transition_to('moving'):
            if pos < 0:
                pos = 0
            elif pos > MAX_RIGHT:
                pos = MAX_RIGHT

            logger.debug(f"Move Trolley to position {pos}cm")
            self.__move_to(pos)
            return self.current_pos
        elif self.current_state.name == 'idle' and self.can_transition_to('stopped'):
            logger.debug(f"Trolley is IDLE, needs to localise prior to moving to position")
            self.transition_to('stopped')
            return self.move_to(pos)

        current_app.logger.critical(f"Trolley state is unexpected: {self.current_state.name}")
        raise Exception

    def __move_to(self, pos):
        required_movement = pos - self.current_pos
        self.transition_to('moving')
        self.stepper.move_relative(required_movement)
        self.transition_to('stopped')
        self.current_pos = pos

    @wrap_in_logs("Localising Trolley", "Trolley is Localised")
    def localise(self):
        self.stepper.motor.goUntilPress(0, 0, 15000)  # (Normally open, left, speed)
        self.stepper.move_right(LIMIT_SWITCH_STANDOFF)
        self.current_pos = LIMIT_SWITCH_STANDOFF


    @wrap_in_logs("Trolley is going idle")
    def idle(self):
        self.stepper.motor.free()
