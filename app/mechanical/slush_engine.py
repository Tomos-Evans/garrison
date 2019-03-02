from app.constants import FAKE_GPIO
from app import logger
from flask import current_app
import time
from app.logging_helpers import wrap_in_logs


class FakeMotor:
    @staticmethod
    def move(amount):
        if not current_app.config['TESTING']:
            time.sleep(1)
        if amount < 0:
            logger.debug(f"Slush Motor moving left {-amount} steps")
            return -amount
        else:
            logger.debug(f"Slush Motor moving right {amount} steps")
            return amount

    @staticmethod
    def isBusy():
        return False


class FakeBoard:
    def setIOState(self, a, b, c):
        pass


if FAKE_GPIO:
    motor = FakeMotor()
    board = FakeBoard()
else:
    import Slush
    from app import constants

    class WrappedBoard:
        def __init__(self, s_board):
            self.s_board = s_board

        def setIOState(self, a, b, c):
            logger.debug(f"Slush Board SetIOState: {a}, {b}, {c}")
            return self.s_board.setIOState(a, b, c)

    class WrappedMotor:
        def __init__(self, s_motor):
            self.s_motor = s_motor

        @wrap_in_logs(after="Slush motor moved")
        def move(self, amount):
            if amount < 0:
                logger.debug(f"Slush Motor moving left {-amount} steps")
                self.s_motor.move(amount)
                return -amount
            else:
                logger.debug(f"Slush Motor moving right {amount} steps")
                self.s_motor.move(amount)
                return amount

        def isBusy(self):
            return self.s_motor.isBusy()


    board = WrappedBoard(Slush.sBoard())
    motor = WrappedMotor(Slush.Motor(constants.MOTOR_NUMBER))
