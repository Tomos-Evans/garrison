from app import db
from flask import url_for
from app.constants import DISPENSER_LOCS
from app.logging_helpers import wrap_in_logs
from app import logger


def optic_dispense():
    from app.mechanical.actuator import actuator

    def f(amount):
        logger.debug(f"Optic dispensing {amount}")
        for _ in range(amount):
            actuator.press()
        return amount
    return f


def test_dispense():
    return lambda a: a


class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=True, index=True, nullable=False)
    position = db.Column(db.Integer, unique=True, index=True, nullable=False)
    dispenser_type = db.Column(db.String(10), index=True)
    disabled = db.Column(db.Boolean(), index=True, nullable=False, default=True)
    volume = db.Column(db.Integer, nullable=False)
    ingredient = db.relationship('Ingredient',  backref='dispenser', uselist=False, lazy='select')

    @classmethod
    def from_params(cls, index, ingredient=None, volume=0, dispenser_type='optic', disabled=True):
        d = cls()
        d.index = index
        d.ingredient = ingredient
        d.volume = volume
        d.dispenser_type = dispenser_type
        d.disabled = disabled
        d.position = DISPENSER_LOCS[index]
        db.session.add(d)
        db.session.commit()

        return d

    @wrap_in_logs("Changing ingredient of dispenser", "Dispenser ingredient changed")
    def change_ingredient(self, ingredient, volume):
        logger.debug(f"Changing dispenser {self.index}")
        self.ingredient = ingredient
        self.volume = volume
        db.session.commit()

    def has(self, amount):
        if amount <= 0:
            raise Exception
        return self.volume >= amount

    def has_used(self, amount):
        assert self.has(amount)
        self.volume -= amount
        db.session.commit()
        return self.volume

    def as_json(self):
        return {
            'location':self.location(),
            'index':self.index,
            'type': self.dispenser_type,
            'disabled': self.disabled,
            'volume':self.volume,
            'ingredient':self.ingredient.location() if self.ingredient else None
        }

    def location(self):
        return url_for('dispensers_dispensers') + str(self.index)

    @wrap_in_logs("Starting Dispense method", "Dispense finished")
    def dispense(self, amount):
        if self.has(amount) and not self.disabled:
            if self.dispenser_type == 'optic':
                dispense_function = optic_dispense()
            else:
                dispense_function = test_dispense()

            used = dispense_function(amount)
            self.volume -= used
            db.session.commit()
            return used
        return None

    @wrap_in_logs("Disabling dispenser", "Dispenser disabled")
    def disable(self):
        self.disabled = True
        self.volume = 0
        self.ingredient = None
        db.session.commit()

    @wrap_in_logs("Enabling dispenser", "Dispenser enabled")
    def enable(self):
        self.disabled = False
        db.session.commit()

    def update_volume(self, volume):
        logger.debug(f"Updating volume of dispenser {self.index}")
        self.volume = volume
        db.session.commit()

    @staticmethod
    @wrap_in_logs("Swapping Dispenser locations", "Dispensers swapped")
    def swap_dispenser_location(d1, d2):
        logger.debug(f"Swapping dispensers {d1.index} and {d2.index}")
        l1 = d1.index
        l2 = d2.index
        d2.index = -1
        db.session.commit()
        d1.index = l2
        d2.index = l1
        db.session.commit()
