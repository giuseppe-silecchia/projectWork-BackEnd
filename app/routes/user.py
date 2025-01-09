from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User
from .. import db

bcrypt = Bcrypt()

#Definisce il modulo per gli utenti
users_bp = Blueprint('users_bp', __name__)

# Endpoint per recuperare le informazioni dell'utente
@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


# Route per ottenere i dettagli di un utente specifico (solo per admin)
@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user_requester_id = get_jwt_identity()
    user_requester = User.query.get_or_404(user_requester_id)

    if not user_requester.isAdmin:
        return jsonify({'message': 'Permission denied'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Endpoint per aggiornare le informazioni dell'utente
@users_bp.route('/users/me', methods=['PATCH'])
@jwt_required()
def update_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    data = request.get_json()
    if 'first_name' in data:
        user.firstName = data['first_name']
    if 'last_name' in data:
        user.lastName = data['last_name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        print('changing password')
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password_hash = hashed_password

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# Endpoint per recueperare le informazioni degli utenti presenti nel sistema
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_system_users():
    user_requester_id = get_jwt_identity()
    user_requester = User.query.get_or_404(user_requester_id)

    #verifica che la richiesta sia stata effettuata da un utente amministratore

    if not user_requester.isAdmin:
        return jsonify({'message': 'Permission denied'}), 403
    
    try:
        users = User.query.all()
        result = [
            user.to_dict()
            for user in users
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


# Route per aggiornare un utente specifico (solo per admin)
@users_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    user_requester_id = get_jwt_identity()
    user_requester = User.query.get_or_404(user_requester_id)

    if not user_requester.isAdmin:
        return jsonify({'message': 'Permission denied'}), 403

    user = User.query.get_or_404(user_id)

    data = request.get_json()
    if 'first_name' in data:
        user.firstName = data['first_name']
    if 'last_name' in data:
        user.lastName = data['last_name']
    if 'email' in data:
        user.email = data['email']
    if 'isAdmin' in data:
        user.isAdmin = data['isAdmin']
    if 'password' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password = hashed_password

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
