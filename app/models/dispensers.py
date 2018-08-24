from abc import abstractmethod
from app import db

class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    ingredient = db.relationship('Ingredient',  backref='dispenser', uselist=False)

    @classmethod
    def from_params(cls, name, ingredient, volume):
        d = cls()
        d.name = name
        d.ingredient = ingredient
        d.volume = volume
        db.session.add(d)
        db.session.commit()

        return d

    def change_ingredient(self, ingredient):
        self.ingredient = ingredient
        db.session.commit()

    def has(self, amount):
        if amount <= 0:
            raise Exception
        return self.volume >= amount

    def has_used(self, amount):
        if amount <= 0:
            raise Exception
        self.volume -= amount
        db.session.commit()
        return self.volume

    @abstractmethod
    def dispense(self, amount):
        raise NotImplementedError
