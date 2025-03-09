from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Вказуємо шлях до папки

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Ініціалізація db у додатку
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():  # Створюємо контекст додатку для реєстрації моделей
        from models import User, Folder  # Імпорт моделей тут
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))  # Використання User після імпорту

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    return app
