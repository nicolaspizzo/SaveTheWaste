from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from savethewaste import db, bcrypt
from savethewaste.pantryIngredients.models import PantryIngredient

pantryIngredients = Blueprint('pantryIngredients', __name__)

@pantryIngredients.route("/viewIngredients", methods=['GET', 'POST'])
def viewIngredient():
    pIng = PantryIngredient.query.all()
    flash("Test")
