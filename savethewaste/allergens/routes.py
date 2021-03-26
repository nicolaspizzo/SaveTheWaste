from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from savethewaste import db
from savethewaste.allergens.models import Allergen
from savethewaste.allergens.forms import AllergenForm

allergens = Blueprint('allergens', __name__)


@allergens.route("/allergens/viewAllergens", methods=['GET', 'POST'])
@login_required
def viewAllergens():
    form = AllergenForm()
    allergens = Allergen.query.filter_by(linkedUserID=current_user.id).first()

    if form.validate_on_submit():
        dairyFree = form.dairyFree.data
        glutenFree = form.glutenFree.data
        vegetarian = form.vegetarian.data
        nutFree = form.nutFree.data
        vegan = form.vegan.data
        allergens.dairyFree = dairyFree
        allergens.glutenFree = glutenFree
        allergens.vegetarian = vegetarian
        allergens.nutFree = nutFree
        allergens.vegan = vegan
        db.session.commit()
        return redirect(url_for('allergens.viewAllergens', form=form, allergens=allergens))
    return render_template('viewAllergens.html', form=form, allergens=allergens)


@allergens.route("/allergens/<int:allergenID>/deleteAllergen", methods=['GET', 'POST'])
@login_required
def deleteAllergen(allergenID):
    allergen = Allergen.query.filter_by(allergenID=allergenID).first()
    db.session.delete(allergen)
    db.session.commit()
    return redirect(url_for('allergens.viewAllergens'))