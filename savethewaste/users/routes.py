from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from savethewaste import db, bcrypt
from savethewaste.users.forms import RegistrationForm, LoginForm
from savethewaste.users.models import User
from savethewaste.pantry.models import Pantry
from savethewaste.allergens.models import Allergen
from datetime import datetime


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() == None:
            hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
            db.session.add(user)
            db.session.commit()
            pantryName = user.username + "'s Pantry"
            pantry = Pantry(name=pantryName, linkedUserID=user.id)
            db.session.add(pantry)
            allergen = Allergen(linkedUserID=user.id)
            db.session.add(allergen)
            db.session.commit()
            flash("Your account has been created!  You are now able to login", 'success')
            return redirect(url_for('users.login'))
        else:
            flash("An account with this email already exists.  Please try again with a different email", 'warning')
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account")
def account():
    return render_template('account.html')

@users.route("/displayUsers")
def displayUsers():
    users = User.query.all()
    render_template('displayUser.html', title='Display Users', users=users)
