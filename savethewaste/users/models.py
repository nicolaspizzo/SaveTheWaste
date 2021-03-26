from savethewaste import db, loginManager
from flask import current_app, flash, Markup
from flask_login import UserMixin


@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    pantry = db.relationship('Pantry', backref="originalUser", lazy=True)
    savedRecipes = db.relationship('Recipe', backref="originalUser", lazy=True)
    allergens = db.relationship('Allergen', backref="originalUser", lazy=True)
    password = db.Column(db.String(60), nullable=False)