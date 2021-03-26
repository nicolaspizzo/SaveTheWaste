from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

class PantryIngredientForm(FlaskForm):
    name = StringField('Name of Ingredient', validators=[DataRequired(), Length(min=2, max=20)])
    quantity = StringField('Quantity', validators=[DataRequired()])
    expiryDate = DateField('Expiration Date')
    submit = SubmitField('Add Ingredient')
