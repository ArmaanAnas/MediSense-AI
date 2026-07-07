from flask import Flask
from config import Config
from app.extensions import db, bcrypt
from app.models import User
from app.routes.main_routes import main

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app