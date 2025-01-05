from flask import Blueprint

from .auth import auth_bp
from .rooms import rooms_bp
from .bookings import bookings_bp
from .user import users_bp


def register_routes(app):
    app.register_blueprint(rooms_bp, url_prefix='/api')
    app.register_blueprint(bookings_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix = '/api')