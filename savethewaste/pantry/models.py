from savethewaste import db
from savethewaste.pantryIngredients.models import PantryIngredient


class Pantry(db.Model):
    pantryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    pantryIngredients = db.relationship('PantryIngredient', backref='originalPantry', lazy=True)
    linkedUserID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def addIngredient(self, form):
        ingName = form.name.data
        quantity = form.quantity.data
        expiryDate = form.expiryDate.data
        ingredient = PantryIngredient(ingredientName=ingName, quantity=quantity, expiryDate=expiryDate,
                                      linkedPantryID=self.pantryID)
        db.session.add(ingredient)
        db.session.commit()
