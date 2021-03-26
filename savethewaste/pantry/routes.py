from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from savethewaste import db, bcrypt
from savethewaste.pantry.models import Pantry
from savethewaste.pantryIngredients.models import PantryIngredient
from savethewaste.pantryIngredients.forms import PantryIngredientForm

pantry = Blueprint('pantry', __name__)

@pantry.route("/pantry", methods=['GET', 'POST'])
@login_required
def viewPantry():
    ingForm = PantryIngredientForm()
    pantry = Pantry.query.filter_by(linkedUserID=current_user.id).first()
    ingredients = PantryIngredient.query.filter_by(linkedPantryID=pantry.pantryID).all()
    if ingForm.validate_on_submit():
        pantry.addIngredient(form=ingForm)
        db.session.commit()
        return redirect(url_for('pantry.viewPantry'))
    return render_template('pantry.html', title="Pantry", pantry=pantry, ingredients=ingredients, form=ingForm)


@pantry.route("/addIngredient", methods=['GET', 'POST'])
@login_required
def addIngredient():
    form = PantryIngredientForm()
    if form.validate_on_submit():
        pantry = Pantry.query.filter_by(linkedUserID=current_user.userID)
        ingredient = PantryIngredient(linkedPantryID=pantry.pantryID, ingredientName=form.ingredientName.data,
                                       quantity=form.quanitity.data, expirationDate=form.expirationDate.data)
        db.session.add(ingredient)
        db.session.commit()
        flash("Ingredient added to your pantry successfully")
        return redirect(url_for('pantry.viewPantry'))
    return render_template('addIngredient.html', title='Pantry', form=form)


@pantry.route("/deleteIngredient/<int:pingID>", methods=['GET', 'POST'])
def deleteIngredient(pingID):
    ingredient = PantryIngredient.query.filter_by(pingID=pingID).first()
    db.session.delete(ingredient)
    db.session.commit()
    flash("Ingredient deleted from pantry", 'success')
    return redirect(url_for('pantry.viewPantry'))


