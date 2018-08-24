from statemachine import StateMachine, State, Transition
from app.constants import HOME_POS, MAX_RIGHT

class Trolley(StateMachine):
    def __init__(self, stepper):
        super().__init__()
        self.add(State('idle', is_starting_state=True, will_enter=self.idle, will_exit=self.localise))
        self.add(State('moving'))
        self.add(State('stopped'))
        self.add(Transition('idle', ['stopped']))
        self.add(Transition('stopped', ['moving', 'idle']))
        self.add(Transition('moving', ['stopped']))

        self.stepper = stepper

        self.go_home()
        self.idle()

    def go_home(self):
        return self.move_to(HOME_POS)

    def move_to(self, pos):
        if self.can_transition_to('moving'):
            if pos < 0:
                self.__move_to(0)
            elif pos > MAX_RIGHT:
                self.__move_to(MAX_RIGHT)
            else:
                self.__move_to(pos)
            return self.current_pos
        elif self.current_state.name == 'idle' and self.can_transition_to('stopped'):
            self.transition_to('stopped')
            return self.move_to(pos)

        raise Exception

    def __move_to(self, pos):
        required_movement = pos - self.current_pos
        self.transition_to('moving')
        self.stepper.move_relative(required_movement)
        self.transition_to('stopped')
        self.current_pos = pos

    def localise(self):
        # move left until the limit switch is reached
        self.current_pos = 0

    def idle(self):
        # Relax the stepper
        pass
