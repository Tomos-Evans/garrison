from statemachine import StateMachine, State, Transition
from app.mechanical import Trolley, Stepper


class BTException(Exception):
    def __init__(self, message):
        self.message = message

    def as_json(self):
        return {
            'error': 'bar tender exception',
            'message': self.message,
        }


class BTBusy(BTException):
    pass


class BTCannotCompleteOrder(BTException):
    pass


class BarTender(StateMachine):
    def __init__(self):
        super().__init__()
        self.add(State('waiting', is_starting_state=True))
        self.add(State('busy'))
        self.add(Transition('waiting', ['busy']))
        self.add(Transition('busy', ['waiting']))

        self.trolley = Trolley(Stepper())

    def make(self, drink):
        if not self.can_make(drink):
            raise BTCannotCompleteOrder('bartender cannot complete that order.')
        if self.is_busy:
            raise BTBusy('cannot make a drink when the bartender is busy.')

        self.transition_to('busy')

        for component in drink.components:
            dispenser = component.ingredient.dispenser
            self.trolley.move_to(dispenser.position)
            dispenser.dispense(component.measure)

        self.trolley.go_home()

        self.transition_to('waiting')

    @staticmethod
    def can_make(drink):
        return any(map(lambda c: c.ingredient.dispenser is not None and
                                 not c.ingredient.dispenser.disabled and
                                 c.measure < c.ingredient.dispenser.volume, drink.components))

    @property
    def is_busy(self):
        return self.current_state.name != 'waiting'

