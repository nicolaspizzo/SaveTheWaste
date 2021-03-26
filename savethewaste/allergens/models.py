from savethewaste import db


class Allergen(db.Model):
    allergenID = db.Column(db.Integer, primary_key=True)
    dairyFree = db.Column(db.Boolean, default=False)
    glutenFree = db.Column(db.Boolean, default=False)
    vegetarian = db.Column(db.Boolean, default=False)
    nutFree = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    linkedUserID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)