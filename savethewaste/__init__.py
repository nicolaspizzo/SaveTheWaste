from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from savethewaste.config import Config



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'


def createApp(configClass=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from savethewaste.allergens.routes import allergens
    from savethewaste.users.routes import users
    from savethewaste.main.routes import main
    from savethewaste.pantry.routes import pantry
    from savethewaste.recipes.routes import recipes
    from savethewaste.pantryIngredients.routes import pantryIngredients
    from savethewaste.errors.handlers import errors

    app.register_blueprint(allergens)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(pantry)
    app.register_blueprint(recipes)
    app.register_blueprint(pantryIngredients)
    app.register_blueprint(errors)


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    loginManager.init_app(app)

    return app