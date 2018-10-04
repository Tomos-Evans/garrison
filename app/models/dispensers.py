from app import db
from flask import url_for

def optic_dispense(amount):
    return amount


class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=True, index=True, nullable=False)
    type = db.Column(db.String(10), index=True)
    volume = db.Column(db.Integer, nullable=False)
    ingredient = db.relationship('Ingredient',  backref='dispenser', uselist=False, lazy='select')

    @classmethod
    def from_params(cls, index, ingredient, volume, type='optic', dispense_function=lambda a: None):
        d = cls()
        d.index = index
        d.ingredient = ingredient
        d.volume = volume
        d.type = type
        db.session.add(d)
        db.session.commit()

        d.dispense_function = dispense_function
        return d

    def change_ingredient(self, ingredient, volume):
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
            'type': self.type,
            'volume':self.volume,
            'ingredient':self.ingredient.location() if self.ingredient else None
        }

    def location(self):
        return url_for('dispensers_dispensers') + str(self.index)

    def dispense(self, amount):
        if self.has(amount):
            self.volume -= amount
            db.session.commit()
            return self.dispense_function(amount)

    def change_type_to(self, type):
        if type=='empty':
            self.type = 'empty'
            self.volume = 0
            self.ingredient = None
            self.dispense_function = lambda a: None
            db.session.commit()
        elif type == 'optic':
            self.type = 'optic'
            self.dispense_function = optic_dispense
            db.session.commit()

    def update_volume(self, volume):
        self.volume = volume
        db.session.commit()

    @staticmethod
    def swap_dispenser_location(d1, d2):
        l1 = d1.index
        l2 = d2.index
        d2.index = -1
        db.session.commit()
        d1.index = l2
        d2.index = l1
        db.session.commit()
