import os

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

from app.db import db_object


def create_app():
    app = Flask(__name__,)

    # Конфигурация
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)

    # Инициализация расширений
    db_object.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Callback для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .blueprints.auth.models import User
        return User.query.get(int(user_id))

    # Регистрация blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.main import main_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp, url_prefix='/')

    # Создание таблиц
    with app.app_context():
        db_object.create_all()

    return app