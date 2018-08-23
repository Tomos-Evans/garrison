import app.constants as constants
from app.mechanical.slush_engine import motor
from flask import current_app

class Stepper():
    def __init__(self):
        self.motor = motor

    def move_relative(self, movement):
        if (movement < 0):
            return self.move_left(-1 * movement)
        else:
            return self.move_right(movement)

    def move_left(self, movement):
        return -self.move_right(movement)

    def move_right(self, movement):
        self.wait_untill_done()
        if current_app.config['TESTING']:
            moved = self.motor.move(int(movement*constants.STEPS_PER_CM), talk=False)
        else:
            moved = self.motor.move(int(movement*constants.STEPS_PER_CM)) # Production motor has not talk argument

        self.wait_untill_done()
        return moved

    def wait_untill_done(self):
        while(self.motor.isBusy()):
            continue
