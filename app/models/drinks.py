from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
    alcoholic = db.Column(db.Boolean(), index=True, nullable=False)
    abs = db.Column(db.Integer())

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
