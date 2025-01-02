from flask import Blueprint
from .rooms import rooms_bp
from .bookings import bookings_bp

def register_routes(app):
    app.register_blueprint(rooms_bp, url_prefix='')
    app.register_blueprint(bookings_bp, url_prefix='')