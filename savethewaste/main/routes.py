from flask import render_template, request, Blueprint, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from savethewaste.pantry.models import Pantry, PantryIngredient
from datetime import datetime, timedelta

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        pantry = Pantry.query.filter_by(linkedUserID=current_user.id).first()
        ingredients = PantryIngredient.query.filter_by(linkedPantryID=pantry.pantryID)
        currentDate = datetime.now()
        for ingredient in ingredients:
            if currentDate < ingredient.expiryDate < currentDate + timedelta(days=2):
                flash("Keep in mind - Ingredient: " + ingredient.ingredientName + " with quantity: " +
                      str(ingredient.quantity) + " will expire on " + str(ingredient.expiryDate.day) + "/" +
                      str(ingredient.expiryDate.month) + "/" + str(ingredient.expiryDate.year) +
                      ". Consider using it in your next recipe! :)", 'warning')
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html')