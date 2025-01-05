from . import db
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # Id univoco dell'entità
    email = db.Column(db.String(80), unique=True, nullable=False)               # Email dell'utente
    password_hash = db.Column(db.String(128), nullable=False)                   # Password (hash) dell'utente
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)            # Relazione con il modello Booking

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "isAdmin": self.isAdmin
        }


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # Id univoco dell'entità
    room_number = db.Column(db.String(10), nullable=False, unique=True)         # Numero della stanza (es. 101)
    max_people = db.Column(db.Integer, nullable=False)                          # Numero massimo ospiti
    bookings = db.relationship('Booking', backref='room', lazy=True)            # Relazione con il modello Booking

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'max_people': self.max_people
        }


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # Id univoco dell'entità
    check_in = db.Column(db.Date, nullable=False)                               # Data check-in della prenotazione
    check_out = db.Column(db.Date, nullable=False)                              # Data check-out della prenotazione
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)   # Chiave esterna che collega la prenotazione a una stanza
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   # Chiave esterna che collega la prenotazione a un utente
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))     # Data e ora in cui è stata creata la prenotazione

    def to_dict(self):
        return {
            'id': self.id,
            'check_in': self.check_in.strftime('%Y-%m-%d'),
            'check_out': self.check_out.strftime('%Y-%m-%d'),
            'room_id': self.room_id
        }