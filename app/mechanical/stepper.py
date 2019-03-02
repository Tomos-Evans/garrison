import app.constants as constants
from app.mechanical.slush_engine import motor
from app import logger
from app.logging_helpers import wrap_in_logs


class Stepper:
    def __init__(self):
        self.motor = motor

    def move_relative(self, movement):
        logger.debug(f"Stepper moving {movement}cm")
        if movement < 0:
            return self.move_left(-movement)
        else:
            return self.move_right(movement)

    @wrap_in_logs(after="Stepper finished")
    def move_left(self, movement):
        logger.debug(f"Stepper moving left {movement}cm")
        self.wait_until_done()
        moved = self.motor.move(int(-movement*constants.STEPS_PER_CM))
        self.wait_until_done()
        return -moved  # TODO Eh? What of earth is happening in this class

    @wrap_in_logs(after="Stepper finished")
    def move_right(self, movement):
        logger.debug(f"Stepper moving right {movement}cm")
        self.wait_until_done()
        moved = self.motor.move(int(movement*constants.STEPS_PER_CM))
        self.wait_until_done()
        return moved

    def wait_until_done(self):
        while self.motor.isBusy():
            continue
