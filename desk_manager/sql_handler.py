from desk_manager import db
from desk_manager.models import Cliente
from app import app
from datetime import datetime


def reset_db():
    with app.app_context():
        db.create_all()
