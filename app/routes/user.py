from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import User
from .. import db

bcrypt = Bcrypt()

users_bp = Blueprint('users_bp', __name__)


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


@users_bp.route('/users/me', methods=['PATCH'])
@jwt_required()
def update_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password = hashed_password

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


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
    if 'username' in data:
        user.username = data['username']
    if 'isAdmin' in data:
        user.role_id = data['isAdmin']
    if 'password' in data:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password = hashed_password

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
