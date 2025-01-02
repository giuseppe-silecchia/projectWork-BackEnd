from app.models import User, db, Room
from flask_bcrypt import Bcrypt


def create_default_user(bcrypt: Bcrypt):
    # Verifica che l'utente "mario.rossi@gmail.com" non esista
    user = User.query.filter_by(email="mario.rossi@gmail.com").first()
    if not user:
        hashed_password = bcrypt.generate_password_hash("Rossi2025").decode('utf-8')
        admin_user = User(
            email="mario.rossi@gmail.com",
            password_hash=hashed_password,
        )
        db.session.add(admin_user)
        db.session.commit()
        print("User created with email 'mario.rossi@gmail.com' and password 'Rossi2025'")


def create_admin_user(bcrypt: Bcrypt):
    # Verifica che l'utente amministratore non esista
    user = User.query.filter_by(email="admin@gmail.com").first()
    if not user:
        hashed_password = bcrypt.generate_password_hash("Admin2025").decode('utf-8')
        admin_user = User(
            email="admin@gmail.com",
            password_hash=hashed_password,
            isAdmin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("User created with email 'admin@gmail.com' and password 'Admin2025'")


def initialize_rooms():
    predefined_rooms = [
        {"room_number": 101, "max_people": 2},
        {"room_number": 102, "max_people": 3},
        {"room_number": 201, "max_people": 2},
        {"room_number": 202, "max_people": 4},
    ]

    # Verifica che le stanze non esistano e in caso le crea.
    for room_data in predefined_rooms:
        existing_room = Room.query.filter_by(room_number=room_data["room_number"]).first()
        if not existing_room:
            new_room = Room(room_number=room_data["room_number"], max_people=room_data["max_people"])
            db.session.add(new_room)

    db.session.commit()
