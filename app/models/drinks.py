import uuid
from app import db
from app.models.dispensers import Dispenser
from flask import url_for

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref =db.Column(db.String(36), nullable=False, default=str(uuid.uuid4()))
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    alcoholic = db.Column(db.Boolean(), index=True, nullable=False)
    abs = db.Column(db.Integer())
    drinkComponents = db.relationship('DrinkComponent',  backref='ingredient', lazy='dynamic')
    dispenser_id      = db.Column(db.Integer, db.ForeignKey('dispenser.id'), nullable=True)

    def __str__(self):
        if self.alcoholic:
            return self.name.title() + " (" + str(self.abs) + "%)"
        else:
            return self.name.title()

    def __repr__(self):
        return "<Ingredient " + self.name + " >"

    @classmethod
    def from_params(cls, name, alcoholic, abs=None):
        if alcoholic and abs == None:
            raise Exception("Alcoholic ingredients must specify their ABS")
        i = cls(name=name, alcoholic=alcoholic, abs=abs)
        db.session.add(i)
        db.session.commit()
        return i

    def as_json(self):
        return {
            'location': url_for('ingredients_ingredients') +self.ref,
            'ref': self.ref,
            'name': self.name,
            'alcoholic': self.alcoholic,
            'abs': self.abs
        }

class DrinkComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    measure = db.Column(db.Integer(), nullable=False)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))

    def __str__(self):
        return str(self.ingredient) + " (" + str(self.measure) + "ml)"

    def __repr__(self):
        return "<DrinkComponent " + str(self.ingredient) + " >"

    @classmethod
    def from_params(cls, ingredient, measure):
        dc = cls(measure=measure)
        dc.ingredient = ingredient
        db.session.add(dc)
        db.session.commit()
        return dc

    def as_json(self):
        return {
            'ingredient': self.ingredient.as_json(),
            'measure': self.measure,
        }

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref =db.Column(db.String(36), nullable=False, default=str(uuid.uuid4()))
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    components = db.relationship('DrinkComponent',  backref='drink', lazy='dynamic')
    alcoholic = db.Column(db.Boolean(), index=True, nullable=False)

    def __str__(self):
        return self.name.title()

    def __iter__(self):
        return self.components.__iter__()

    @classmethod
    def from_params(cls, name, components):
        alc_list = map(lambda c: c.ingredient.alcoholic, components)

        d = cls(name=name, alcoholic=True in alc_list)
        d.components = components

        db.session.add(d)
        db.session.commit()
        return d

    def as_json(self):
        return {
            'location': url_for('drinks_drinks') +self.ref,
            'ref': self.ref,
            'name': self.name,
            'components': [c.as_json() for c in self.components]
        }
