from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, session
import requests
from bs4 import BeautifulSoup
from flask_login import login_user, current_user, logout_user, login_required
from savethewaste import db, bcrypt
from savethewaste.allergens.models import Allergen
from savethewaste.pantry.models import Pantry
from savethewaste.recipes.models import Recipe
from savethewaste.recipes.forms import SaveRecipeForm, FindRecipe
from savethewaste.pantryIngredients.models import PantryIngredient
from datetime import datetime
from savethewaste.recipes.utils import bbcWebScraperSearch, bbcWebScraperRecipe, tescoWebScraperSearch, tescoWebScraperRecipe, \
    sainsburyWebScraperSearch, sainsburyWebScraperRecipe, getIngredients, resetSession
from flask_mail import Message


recipes = Blueprint('recipes', __name__)

# BBC Section

recipeCount = 8

@recipes.route("/recipe/findRecipe/bbc",  methods=['GET', 'POST'])
def findRecipeBBC():
    resetSession()
    form = FindRecipe()
    pantryID = Pantry.query.filter_by(originalUser=current_user).first().pantryID
    currentIngredients = PantryIngredient.query.filter_by(linkedPantryID=pantryID).all()
    jsIngredientList = []
    for ingredient in currentIngredients:
        jsIngredientList.append(ingredient.ingredientName)
    if request.method == 'POST':
        ingredients = []
        inputIngredients = request.form.getlist('mytext[]')
        for ingredient in inputIngredients:
            ingredients.append(ingredient)
        session['ingredients'] = ingredients
        return redirect(url_for('recipes.viewRecipeSearchBBC'))
    return render_template('findRecipe.html', title='Find Recipe', form=form, jsIngredientList=jsIngredientList, name="BBC")


@recipes.route("/recipe/viewRecipeSearch/bbc", methods=['GET', 'POST'])
def viewRecipeSearchBBC():
    ingredients = session['ingredients']
    bbcRecipes = bbcWebScraperSearch(ingredients, recipeCount)
    for recipe in bbcRecipes:
        name = recipe.recipeName
        url = recipe.url
        session[name] = [url, recipe.bbc, recipe.tesco, recipe.sain]

    return render_template('displaySearchRecipes.html', title='Recipe Search Results', recipes=bbcRecipes, name='BBC')


# Tesco Section

@recipes.route("/recipe/findRecipe/tesco",  methods=['GET', 'POST'])
def findRecipeTesco():
    resetSession()
    form = FindRecipe()
    pantryID = Pantry.query.filter_by(originalUser=current_user).first().pantryID
    currentIngredients = PantryIngredient.query.filter_by(linkedPantryID=pantryID).all()
    jsIngredientList = []
    for ingredient in currentIngredients:
        jsIngredientList.append(ingredient.ingredientName)
    if request.method == 'POST':
        ingredients = []
        inputIngredients = request.form.getlist('mytext[]')
        for ingredient in inputIngredients:
            ingredients.append(ingredient)
        session['ingredients'] = ingredients
        return redirect(url_for('recipes.viewRecipeSearchTesco'))
    return render_template('findRecipe.html', title='Find Recipe', form=form, jsIngredientList=jsIngredientList, name="Tesco")


@recipes.route("/recipe/viewRecipeSearch/tesco", methods=['GET', 'POST'])
def viewRecipeSearchTesco():
    ingredients = session['ingredients']
    tescoRecipes = tescoWebScraperSearch(ingredients, recipeCount)
    for recipe in tescoRecipes:
        name = recipe.recipeName
        url = recipe.url
        session[name] = [url, recipe.bbc, recipe.tesco, recipe.sain]
    flash(session)
    return render_template('displaySearchRecipes.html', title='Recipe Search Results', recipes=tescoRecipes, name='Tesco')




# Sainsbury's Section

@recipes.route("/recipe/findRecipe/sainsbury",  methods=['GET', 'POST'])
def findRecipeSainsbury():
    resetSession()
    form = FindRecipe()
    pantryID = Pantry.query.filter_by(originalUser=current_user).first().pantryID
    currentIngredients = PantryIngredient.query.filter_by(linkedPantryID=pantryID).all()
    jsIngredientList = []
    for ingredient in currentIngredients:
        jsIngredientList.append(ingredient.ingredientName)
    if request.method == 'POST':
        ingredients = []
        inputIngredients = request.form.getlist('mytext[]')
        for ingredient in inputIngredients:
            ingredients.append(ingredient)
        session['ingredients'] = ingredients
        return redirect(url_for('recipes.viewRecipeSearchSainsbury'))
    return render_template('findRecipe.html', title='Find Recipe', form=form, jsIngredientList=jsIngredientList, name="Sainsbury\'s")


@recipes.route("/recipe/viewRecipeSearch/sainsbury", methods=['GET', 'POST'])
def viewRecipeSearchSainsbury():
    ingredients = session['ingredients']
    sainsburyRecipes = sainsburyWebScraperSearch(ingredients, recipeCount)
    for recipe in sainsburyRecipes:
        name = recipe.recipeName
        url = recipe.url
        session[name] = [url, recipe.bbc, recipe.tesco, recipe.sain]
    return render_template('displaySearchRecipes.html', title='Recipe Search Results', recipes=sainsburyRecipes, name='Sainsbury\'s')


# All recipes

@recipes.route("/recipe/findRecipe/all",  methods=['GET', 'POST'])
def findRecipeAll():
    resetSession()
    form = FindRecipe()
    pantryID = Pantry.query.filter_by(originalUser=current_user).first().pantryID
    currentIngredients = PantryIngredient.query.filter_by(linkedPantryID=pantryID).all()
    jsIngredientList = []
    for ingredient in currentIngredients:
        jsIngredientList.append(ingredient.ingredientName)
    if request.method == 'POST':
        ingredients = []
        inputIngredients = request.form.getlist('mytext[]')
        for ingredient in inputIngredients:
            ingredients.append(ingredient)
        session['ingredients'] = ingredients
        return redirect(url_for('recipes.viewRecipeSearchAll'))
    return render_template('findRecipe.html', title='Find Recipe', form=form, jsIngredientList=jsIngredientList)


@recipes.route("/recipe/viewRecipeSearch/all", methods=['GET', 'POST'])
def viewRecipeSearchAll():
    ingredients = session['ingredients']
    bbcRecipes = bbcWebScraperSearch(ingredients, 5)
    tescoRecipes = tescoWebScraperSearch(ingredients, 5)
    sainsburyRecipes = sainsburyWebScraperSearch(ingredients, 5)
    allRecipes = []
    allRecipes.append(bbcRecipes)
    allRecipes.append(tescoRecipes)
    allRecipes.append(sainsburyRecipes)
    for i in range(0, 3):
        for recipe in allRecipes[i]:
            name = recipe.recipeName
            url = recipe.url
            session[name] = [url, recipe.bbc, recipe.tesco, recipe.sain]
    return render_template('displayAllSearchRecipes.html', title='Recipe Search Results', bbcRecipes=bbcRecipes,
                           tescoRecipes=tescoRecipes, sainsburyRecipes=sainsburyRecipes)


# View Functions

@recipes.route("/recipe/viewRecipe/<recipeName>", methods=['GET', 'POST'])
def viewRecipe(recipeName):
    saveRecipe = SaveRecipeForm()
    recipeURL = session[recipeName][0]
    bbc = False
    tesco = False
    sain = False
    if session[recipeName][1] is True:
        individualRecipe = bbcWebScraperRecipe(recipeURL)
        bbc = True
    elif session[recipeName][2] is True:
        individualRecipe = tescoWebScraperRecipe(recipeURL)
        tesco = True
    else:
        individualRecipe = sainsburyWebScraperRecipe(recipeURL)
        sain = True
    if saveRecipe.validate_on_submit():
        recipe = Recipe(recipeName=individualRecipe.recipeName, date=datetime.today(),
                        url=individualRecipe.url, userID=current_user.id, bbc=bbc, tesco=tesco, sain=sain)
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe saved successfully!", 'success')
    return render_template('viewRecipe.html', title='Find Recipe', recipe=individualRecipe, form=saveRecipe)


@recipes.route("/recipe/displaySavedRecipes")
def displaySavedRecipes():
    recipes = Recipe.query.filter_by(userID=current_user.id).all()
    return render_template('savedRecipes.html', title='Display Recipes', recipes=recipes)


@recipes.route("/recipe/viewSavedRecipe/<recipeName>")
def viewSavedRecipe(recipeName):
    recipe = Recipe.query.filter_by(recipeName=recipeName).first()
    url = recipe.url
    if recipe.bbc == True:
        individualRecipe = bbcWebScraperRecipe(url)
    elif recipe.tesco == True:
        individualRecipe = tescoWebScraperRecipe(url)
    else:
        individualRecipe = sainsburyWebScraperRecipe(url)
    return render_template('viewSavedRecipe.html', title='Find Recipe', recipe=individualRecipe, dbRecipe=recipe)


@recipes.route("/recipe/deleteRecipe/<int:recipeID>", methods=['GET', 'POST'])
def deleteRecipe(recipeID):
    recipe = Recipe.query.filter_by(recipeID=recipeID).first()
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe successfully deleted", 'success')
    return redirect(url_for('recipes.displaySavedRecipes'))