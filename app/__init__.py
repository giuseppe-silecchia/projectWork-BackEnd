from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import datetime
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/api/*": {"origins": ["*", "http://localhost:4200"], "methods": ["PUT", "POST", "GET", "PATCH", "DELETE"],
                    "max_age": 6000}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    app.config['JWT_SECRET_KEY'] = '636f3dc78f7924c396e28a336c6f1'  # Definisce la chiave segreta usata dall'app Flask.
    app.config['JWT_VERIFY_SUB'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=2)  # Definisce la durata (validità) del token

    jwt = JWTManager(app)  # Configura Flask-JWT-Extended con l'app per gestire l'autenticazione tramite token JWT.

    db.init_app(app)

    from .routes import register_routes
    register_routes(app)

    return app
