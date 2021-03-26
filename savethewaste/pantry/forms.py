from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

class RegistrationForm(FlaskForm):
    ingredientName = StringField('Name of Ingredient', validators=[DataRequired(), Length(min=2, max=20)])
    quantity = StringField('Quantity', validators=[DataRequired(), Email()])
    expirationDate = IntegerField('Expiration Date', validators=[DataRequired()])
    submit = SubmitField('Add Ingredient')
