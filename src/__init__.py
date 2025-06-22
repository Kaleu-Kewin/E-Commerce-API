import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

CORS(app)

from src.routes import auth_routes, products_routes
