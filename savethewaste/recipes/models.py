from savethewaste import db, loginManager

class Recipe(db.Model):
    recipeID = db.Column(db.Integer, primary_key=True)
    recipeName = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime())
    url = db.Column(db.String(100), unique=True, nullable=False)
    bbc = db.Column(db.Boolean, default=False)
    tesco = db.Column(db.Boolean, default=False)
    sain = db.Column(db.Boolean, default=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))

