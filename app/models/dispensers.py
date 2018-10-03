from abc import abstractmethod
from app import db

class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, unique=True, index=True, nullable=False)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    ingredient = db.relationship('Ingredient',  backref='dispenser', uselist=False)

    @classmethod
    def from_params(cls, index, name, ingredient, volume):
        d = cls()
        d.index = index
        d.name = name
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
            'index': self.index,
            'name': self.name,
            'volume': self.volume,
            'ingredient': self.ingredient.location()
        }

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
