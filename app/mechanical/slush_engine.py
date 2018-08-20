from app import app

if app.config['FAKE_GPIO']:
    class FakeMotor:
        def move(self, amount):
            if amount<0:
                print("Slush Engine moving left", -amount, "steps")
            else:
                print("Slush Engine moving right", + amount, "steps")
            return amount
    motor = FakeMotor()
else:
    import Slush
    board = Slush.sBoard()
    motor = Slush.Motor(0) # The motor number
