import app.constants as constants
from app.mechanical.slush_engine import motor


class Stepper:
    def __init__(self):
        self.motor = motor

    def move_relative(self, movement):
        if movement < 0:
            return self.move_left(-1 * movement)
        else:
            return self.move_right(movement)

    def move_left(self, movement):
        return -self.move_right(movement)

    def move_right(self, movement):
        self.wait_until_done()
        moved = self.motor.move(int(movement*constants.STEPS_PER_CM))

        self.wait_until_done()
        return moved

    def wait_until_done(self):
        while self.motor.isBusy():
            continue
