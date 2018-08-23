from app.constants import FAKE_GPIO
if FAKE_GPIO:
    class FakeMotor:
        def move(self, amount, talk=True):
            if talk:
                if amount<0:
                    print("Slush Engine moving left", -amount, "steps")
                else:
                    print("Slush Engine moving right", + amount, "steps")
            return amount
    motor = FakeMotor()
else:
    import Slush
    board = Slush.sBoard()
    motor = Slush.Motor(0)
