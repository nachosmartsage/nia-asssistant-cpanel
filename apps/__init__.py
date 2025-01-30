from flask import Flask
from flask_pymongo import PyMongo
from importlib import import_module
from flask_login import LoginManager

mongo = PyMongo()
# Configura el LoginManager
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def register_extensions(app):
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    mongo.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    return app


def get_db():
    return mongo.db

