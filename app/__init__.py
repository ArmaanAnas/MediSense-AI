from flask import Flask
from config import Config
from app.routes.auth_routes import auth
from app.routes.prediction_routes import prediction
from app.routes.heart_prediction_routes import heart_prediction
from app.routes.recommendation_routes import recommendation
from app.routes.chatbot_routes import chatbot

from app.extensions import (
    db,
    bcrypt,
    login_manager
)

from app.models import User
from app.routes.main_routes import main

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(heart_prediction)
    app.register_blueprint(prediction)
    app.register_blueprint(recommendation)
    app.register_blueprint(chatbot)

    with app.app_context():
        db.create_all()

    return app