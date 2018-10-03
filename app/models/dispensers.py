from abc import abstractmethod
from app import db
from flask import url_for

class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=True, index=True, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    ingredient = db.relationship('Ingredient',  backref='dispenser', uselist=False, lazy='select')

    @classmethod
    def from_params(cls, index, ingredient, volume):
        d = cls()
        d.index = index
        d.ingredient = ingredient
        d.volume = volume
        db.session.add(d)
        db.session.commit()

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
            'volume':self.volume,
            'ingredient':self.ingredient.location()
        }

    def location(self):
        return url_for('dispensers_dispensers') + str(self.index)

    @abstractmethod
    def dispense(self, amount):
        raise NotImplementedError

    @staticmethod
    def swap_dispenser_location(d1, d2):
        l1 = d1.index
        l2 = d2.index
        d2.index = -1
        db.session.commit()
        d1.index = l2
        d2.index = l1
        db.session.commit()
