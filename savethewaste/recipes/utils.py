from flask import url_for, flash, request, Blueprint, abort, session
import requests
import time
import re
import pprint
from bs4 import BeautifulSoup
from flask_login import current_user
from savethewaste import db, bcrypt
from savethewaste.allergens.models import Allergen
from savethewaste.recipes.models import Recipe
from datetime import datetime
import json

class SearchRecipes():
    def __init__(self, recipeName, url, bbc, tesco, sain):
        self.recipeName = recipeName
        self.url = url
        self.bbc = bbc
        self.tesco = tesco
        self.sain = sain

    def as_dict(self):
        return {"id": self.id, "name": self.recipeName, "url": self.url}


class IndividualRecipe():
    def __init__(self, recipeName, date, url, recipeIngredients, ingredientQuantity, facts, description, instructions, rating):
        self.recipeName = recipeName
        self.date = date
        self.url = url
        self.recipeIngredients = recipeIngredients
        self.ingredientQuantity = ingredientQuantity
        self.description = description
        self.instructions = instructions
        self.facts = facts
        self.rating = rating

    def as_dict(self):
        return {"name": self.recipeName, "date": str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year),
                "url": self.url, "ingredients": self.recipeIngredients, "ingredientQuantity": self.ingredientQuantity,
                "description": self.description, "instructions": self.instructions, "facts": self.facts, "rating": self.rating}



def bbcWebScraperSearch(ingredients, recipeCount):
    ingredientsString = '?q='

    for i in range(len(ingredients)):
        ingredientsString += ingredients[i] + '+'

    allergens = Allergen.query.filter_by(linkedUserID=current_user.id).first()
    allergen = ""
    if allergens.dairyFree == True:
       allergen = allergen + "&diet=" + "dairy-free"
    if allergens.glutenFree == True:
       allergen = allergen + "&diet=" + "gluten-free"
    if allergens.nutFree == True:
       allergen = allergen +  "&diet=" + "nut-free"
    if allergens.vegetarian == True:
       allergen = allergen +  "&diet=" + "vegetarian"
    if allergens.vegan == True:
       allergen = allergen + "&diet=" + "vegan"

    URL = 'https://www.bbcgoodfood.com/search/recipes' + ingredientsString + allergen
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    recipes = soup.select('div.col-12.template-search-universal__card')
    recipeResults = []
    for i in range(len(recipes)):
        if i > recipeCount:
            break
        recipe = recipes[i]
        name = recipe.find(class_='standard-card-new__article-title')
        nameText = name.get_text()

        recipeURL = "https://www.bbcgoodfood.com" + name.get("href")

        newRecipe = SearchRecipes(recipeName=nameText, url=recipeURL, bbc=True, tesco=False, sain=False)
        recipeResults.append(newRecipe)
    page.close()
    return recipeResults


def bbcWebScraperRecipe(recipeURL):
    recipePage = requests.get(recipeURL)
    recipeSoup = BeautifulSoup(recipePage.content, 'html.parser')

    recipeDetails = recipeSoup.find(class_="post recipe")
    description = recipeDetails.find(class_='editor-content').get_text()

    name = recipeDetails.find(class_="post-header__title").get_text()

    ratingGroup = recipeDetails.find(class_="rating__values")
    rating = ratingGroup.find(class_="sr-only").get_text()

    facts = recipeDetails.find_all(class_="mb-sm mr-xl list-item")
    factsList = []
    for i in range(0, len(facts)):
        factsList.append(facts[i].get_text())

    facts = recipeDetails.find_all(class_="mb-sm list-item")
    for i in range(0, len(facts)):
        factsList.append(facts[i].get_text())

    factsList[0] = factsList[0].replace("Preparation and cooking time", "")
    factsList[0] = factsList[0].replace("mins", " ")

    ingredients = recipeSoup.select('li.pb-xxs.pt-xxs.list-item.list-item--separator')
    ingredientList = []
    for i in range(len(ingredients)):
        ingredient = ingredients[i]
        ingredientList.append(ingredient.get_text())

    steps = recipeSoup.select('li.pb-xs.pt-xs.list-item')
    instructionList = []
    for i in range(len(steps)):
        step = steps[i]
        string = step.get_text().replace('\xa0', "")
        counter = 0
        numLength = 0
        for i in string:
            if counter > 4:
                if i.isdigit():
                    numLength += 1
                else:
                    break
            counter += 1
        string = string[numLength + 5:]
        instructionList.append(string)
    ingredientQuantityList = []
    newRecipe = IndividualRecipe(recipeName=name, date=datetime.today(), url=recipeURL,
                                 recipeIngredients=ingredientList, ingredientQuantity=ingredientQuantityList,
                                 instructions=instructionList, rating=rating,
                                 facts=factsList, description=description)
    recipePage.close()
    return newRecipe


def sainsburyWebScraperSearch(ingredients, recipeCount):
    term = ''
    count = 0
    for ingredient in ingredients:
        if count == 0:
            term = ingredient
            count = count + 1
        else:
            term = term + '+' + ingredient
            count = count + 1

    allergens = Allergen.query.filter_by(linkedUserID=current_user.id).first()
    allergen = ""
    if allergens.dairyFree == True:
        allergen = allergen + "&tag_slugs%5B%5D=" + "dairy-free"
    if allergens.glutenFree == True:
        allergen = allergen + "&tag_slugs%5B%5D=" + "gluten-free"
    if allergens.nutFree == True:
        allergen = allergen + "&tag_slugs%5B%5D=" + "nut-free"
    if allergens.vegetarian == True:
        allergen = allergen + "&tag_slugs%5B%5D=" + "vegetarian"
    if allergens.vegan == True:
        allergen = allergen + "&tag_slugs%5B%5D=" + "vegan"


    URL = "https://recipes.sainsburys.co.uk/search?sort_by=relevant&tab=recipes" + allergen + "&term=" + term
    baseURL = "https://recipes.sainsburys.co.uk"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="results")

    recipes = results.find_all(class_="block")
    recipeResults = []
    for i in range(0, len(recipes)):
        if i > recipeCount:
            break
        recipe = recipes[i]
        name = recipe.find(class_="like-title")
        nameText = name.get_text()

        recipeURL = baseURL + name['href']

        newRecipe = SearchRecipes(recipeName=nameText, url=recipeURL, bbc=False, tesco=False, sain=True)

        recipeResults.append(newRecipe)
    page.close()
    return recipeResults


def sainsburyWebScraperRecipe(url):
    recipeURL = url
    recipePage = requests.get(recipeURL)
    recipeSoup = BeautifulSoup(recipePage.content, 'html.parser')

    name = recipeSoup.find(class_="like-title")
    nameText = name.get_text()

    recipeDetails = recipeSoup.find(class_="recipe-header")
    description = recipeDetails.find(class_="summary").get_text()

    facts = recipeDetails.find_all(class_="facts-content")
    factsList = []
    for j in range(0, len(facts)):
        factsList.append(facts[j].get_text())
    rating = recipeDetails.find(class_="amount_liked").get_text()

    ingredientSection = recipeSoup.find(class_="ingredients-list")
    # ingredients = ingredientSection.find_all(class_="ingredient-label")
    ingredients = ingredientSection.find_all('li')
    ingredientQuantity = ingredientSection.find_all(class_="ingredient-amount")
    ingredientList = []
    ingredientQuantityList = []
    measurements = []

    for m in range(0, len(ingredients)):
        ingredient = ingredients[m].get_text()
        ingredient = ingredient[1:len(ingredient) - 1]
        ingredientList.append(ingredient)

    instructionSection = recipeSoup.find(class_='e-instructions')
    instructions = instructionSection.find_all(class_="instruction-txt")
    instructionList = []
    for k in range(0, len(instructions)):
        instructionList.append(instructions[k].get_text())

    newRecipe = IndividualRecipe(recipeName=nameText, date=datetime.today(), url=recipeURL,
                             recipeIngredients=ingredientList, ingredientQuantity=ingredientQuantityList,
                             instructions=instructionList, rating=rating,
                             facts=factsList, description=description)
    recipePage.close()
    return newRecipe


def tescoWebScraperSearch(ingredients, recipeCount):
    allergens = Allergens = Allergen.query.filter_by(linkedUserID=current_user.id).first()
    allergen = ""
    URL = 'https://realfood.tesco.com/search.html?search='

    for x in range(0, len(ingredients)):
        if x == 0:
            URL = URL + ingredients[x]
        else:
            URL = URL + '%20' + ingredients[x]

    if allergens.dairyFree == True:
      allergen = allergen + "&DietaryOption=" + "Dairy-free"
    if allergens.glutenFree == True:
      allergen = allergen + "&DietaryOption=" + "Gluten-free"
    if allergens.nutFree == True:
      flash("Note: Tesco does not filter recipes without nuts, PLEASE double check ingredients")
    if allergens.vegetarian == True:
      allergen = allergen + "&DietaryOption=" + "Vegetarian"
    if allergens.vegan == True:
      allergen = allergen + "&DietaryOption=" + "Vegan"

    URL = URL + allergen
    flash(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    recipe_results = soup.find_all('li', class_='ddl-search-results__item')

    valid_recipe = []
    searched_recipes = []

    for recipe in recipe_results:
        results = recipe.find('div', class_='ddl-search-results__rating')
        try:
            temp = results.get_text()
            valid_recipe.append(recipe)
        except:
            temp = "none"
    count = 0
    for recipes in valid_recipe:
        if count > recipeCount:
            break
        recipe_name = (recipes.find('h2', class_="ddl-search-results__item-heading")).get_text()
        recipe_link = "https://realfood.tesco.com" + (recipes.find('a', class_='ddl-search-results__item-link'))['href']

        newRecipe = SearchRecipes(recipeName=recipe_name, url=recipe_link, bbc=False, tesco=True, sain=False)
        searched_recipes.append(newRecipe)
        count = count + 1
    page.close()
    return searched_recipes


def tescoWebScraperRecipe(url):
    ingredientsquantity = []
    description = ""
    temp_ingredient = []
    temp_method = ""
    URL_recipe = url
    recipe_page = requests.get(url)
    soup2 = BeautifulSoup(recipe_page.content, 'html.parser')

    all_ingredients = soup2.find_all('li', class_='recipe-detail__list-item')
    all_instructions = soup2.find('div', class_='recipe-detail__cms')

    recipe_name = (soup2.find('h1', class_='recipe-detail__headline')).get_text()
    rating_block = soup2.find_all('button', class_='recipe-detail__rate-star recipe-detail__rate-star_active')

    servings = soup2.find('ul', class_='recipe-detail__meta')
    indServing = servings.find_all(class_="recipe-detail__meta-item_servings")
    factsList = []
    for k in range(0, len(indServing)):
        factsList.append(indServing[k].get_text())

    for item in all_ingredients:
        temp = item.get_text()
        temp_ingredient.append(temp)

    rating_num = "Rating: " + str(len(rating_block)) + " out of 5"

    instructions = all_instructions.find_all('li')
    recipeInstructions = []
    for instruction in instructions:
        recipeInstructions.append(instruction.get_text())
    newRecipe = IndividualRecipe(recipeName=recipe_name, date=datetime.today(), url=URL_recipe,
                                 recipeIngredients=temp_ingredient, ingredientQuantity=ingredientsquantity,
                                 instructions=recipeInstructions, rating=rating_num,
                                 facts=factsList, description=description)
    recipe_page.close()
    return newRecipe


def getIngredients(form):
    ingredients = []
    if form.ingredient1.data:
        ingredients.append(form.ingredient1.data)
    if form.ingredient2.data:
        ingredients.append(form.ingredient2.data)
    if form.ingredient3.data:
        ingredients.append(form.ingredient3.data)
    if form.ingredient4.data:
        ingredients.append(form.ingredient4.data)
    if form.ingredient5.data:
        ingredients.append(form.ingredient5.data)
    return ingredients


def resetSession():
    for key in list(session.keys()):
        if key != '_fresh' and key != '_id' and key != '_user_id' and key != 'csrf_token' and key != 'ingredients':
            session.pop(key)
