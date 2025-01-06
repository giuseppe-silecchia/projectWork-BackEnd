from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User
from .. import db

auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    firstName = data.get('firstName')
    lastName = data.get('lastName')

    if not firstName or not lastName:
        return jsonify({"message": "First name and last Name are required"}), 400

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    # Verifica che l'email non esista già
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    # Verifica che la nuova password sia sufficientemente lunga (minimo 8 caratteri)
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    # Crea un nuovo utente e cifra la password
    new_user = User(email=email, firstName=firstName, lastName=lastName)
    new_user.set_password(password)

    # Salva l'utente nel database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/update-password', methods=['PATCH'])
@jwt_required()
def update_password():
    try:
        current_user_id = get_jwt_identity()  # Ottieni l'ID dell'utente dal token JWT
        data = request.get_json()

        # Verifica che i dati siano validi
        if 'current_password' not in data or 'new_password' not in data:
            return jsonify({'message': 'Current password and new password are required'}), 400

        current_password = data['current_password']
        new_password = data['new_password']

        # Trova l'utente nel database
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Verifica che la password corrente sia corretta
        if not bcrypt.check_password_hash(user.password_hash, current_password):
            return jsonify({'message': 'Current password is incorrect'}), 400

        # Verifica che la nuova password sia sufficientemente lunga (ad esempio, minimo 8 caratteri)
        if len(new_password) < 8:
            return jsonify({'message': 'New password must be at least 8 characters long'}), 400

        # Cifra la nuova password
        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Aggiorna la password dell'utente nel database
        user.password_hash = hashed_new_password
        db.session.commit()

        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
