from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app(debug=False):
    app = Flask(__name__, template_folder='../app/Templates')

    app.config.from_object(Config) 
    login.login_view = 'main.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)
    login.init_app(app)

    migrate = Migrate(app, db)
    return app

