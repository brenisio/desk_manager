from flask import Flask
from .extensions import db
from .blueprints import registrar_blueprints
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.static_folder = 'static'
    db.init_app(app)
    registrar_blueprints(app)
    return app


