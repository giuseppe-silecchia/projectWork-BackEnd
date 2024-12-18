from . import db
from datetime import datetime, timezone


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # Id univoco dell'entità
    room_number = db.Column(db.String(10), nullable=False, unique=True)         # Numero della stanza (es. 101)
    max_people = db.Column(db.Integer, nullable=False)                          # Numero massimo ospiti
    bookings = db.relationship('Booking', backref='room', lazy=True)            # relazione (collegamento con il modello Booking)

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'max_people': self.max_people
        }


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                # Id univoco dell'entità
    customer_name = db.Column(db.String(50), nullable=False)                    # Nome del cliente che ha prenotato
    check_in = db.Column(db.Date, nullable=False)                               # Data check-in della prenotazione
    check_out = db.Column(db.Date, nullable=False)                              # Data check-out della prenotazione
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)   # Chiave esterna che collega la prenotazione a una stanza
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))     # Data e ora in cui è stata creata la prenotazione

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'check_in': self.check_in.strftime('%Y-%m-%d'),
            'check_out': self.check_out.strftime('%Y-%m-%d'),
            'room_id': self.room_id
        }