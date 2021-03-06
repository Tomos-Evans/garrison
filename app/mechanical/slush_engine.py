from app.constants import FAKE_GPIO

class FakeMotor:
    def move(self, amount, talk=True):
        if amount<0:
            if talk:
                print("Slush Engine moving left", -amount, "steps")
            return -amount
        else:
            if talk:
                print("Slush Engine moving right", + amount, "steps")
            return amount

    def isBusy(self):
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
    board = Slush.sBoard()
    motor = Slush.Motor(constants.MOTOR_NUMBER)
