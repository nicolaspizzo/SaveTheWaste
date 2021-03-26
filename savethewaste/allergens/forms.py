from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class AllergenForm(FlaskForm):
    dairyFree = BooleanField(label="Dairy Free")
    glutenFree = BooleanField(label="Gluten Free")
    vegetarian = BooleanField(label="Vegetarian")
    nutFree = BooleanField(label="Nut Free")
    vegan = BooleanField(label="Vegan")
    submit = SubmitField('Add Allergen to profile')
