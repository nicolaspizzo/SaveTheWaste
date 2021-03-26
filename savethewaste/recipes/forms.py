from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


class SaveRecipeForm(FlaskForm):
    submit = SubmitField('Save')


class FindRecipe(FlaskForm):
    ingredient1 = StringField('Ingredient 1', validators=[DataRequired(), Length(min=2, max=20)])
    ingredient2 = StringField('Ingredient 2')
    ingredient3 = StringField('Ingredient 3')
    ingredient4 = StringField('Ingredient 4')
    ingredient5 = StringField('Ingredient 5')
    submit = SubmitField('Search')