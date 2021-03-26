from savethewaste import db, loginManager

class PantryIngredient(db.Model):
    pingID = db.Column(db.Integer, primary_key=True)
    ingredientName = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(20), nullable=False)
    expiryDate = db.Column(db.DateTime, nullable=False)
    linkedPantryID = db.Column(db.Integer, db.ForeignKey('pantry.pantryID'), nullable=False)

