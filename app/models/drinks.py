from app import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    alcoholic = db.Column(db.Boolean(), index=True, nullable=False)
    abs = db.Column(db.Integer())

    drinkComponents = db.relationship('DrinkComponent',  backref='ingredient', lazy='dynamic')

    def __str__(self):
        if self.alcoholic:
            return self.name.title() + " (" + str(self.abs) + "%)"
        else:
            return self.name.title()
    def __repr__(self):
        return "<Ingredient " + self.name + ">"

    @classmethod
    def from_params(cls, name, alcoholic, abs=None):
        if alcoholic and abs == None:
            raise Exception("Alcoholic ingredients must specify their ABS")
        i = cls(name=name, alcoholic=alcoholic, abs=abs)
        db.session.add(i)
        db.session.commit()
        return i

class DrinkComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'))
    measure = db.Column(db.Integer(), nullable=False)

    def __str__(self):
        return str(self.measure) + "ml " + str(self.ingredient)

    @classmethod
    def from_params(cls, ingredient, measure):
        dc = cls(measure=measure)
        dc.ingredient = ingredient
        db.session.add(dc)
        db.session.commit()
        return dc

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    components = db.relationship('DrinkComponent',  backref='drink', lazy='dynamic')

    def __str__(self):
        return self.name.title()
    @classmethod
    def from_params(cls, name, components):
        d = cls(name=name)
        for c in components:
            d.components.append(c)
        db.session.add(d)
        db.session.commit()
        return d
