from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Booking
from .. import db
from datetime import datetime

bookings_bp = Blueprint('bookings_bp', __name__)


@bookings_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    try:
        bookings = Booking.query.all()
        result = [booking.to_dict() for booking in bookings]
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@bookings_bp.route('/bookings/<int:id>', methods=['GET'])
@jwt_required()
def get_booking(id: int):
    booking = Booking.query.get_or_404(id)
    result = booking.to_dict()
    return jsonify(result)


@bookings_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        current_user_id = get_jwt_identity()  # ID dell'utente autenticato
        data = request.get_json()

        # Check del formato delle date
        try:
            check_in_date = datetime.strptime(data['check_in'], '%Y-%m-%d')
            check_out_date = datetime.strptime(data['check_out'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Check se la data di check-out è dopo la data di check-in
        if check_in_date >= check_out_date:
            return jsonify({'message': 'Check-out date must be after check-in date'}), 400

        # Controlla se la stanza è già prenotata per il periodo richiesto
        room_id = data['room_id']

        conflicting_booking = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.check_in < check_out_date,
            Booking.check_out > check_in_date
        ).first()

        if conflicting_booking:
            return jsonify({'message': 'Room is already booked for the selected dates'}), 400

        # 6. Crea la prenotazione
        new_booking = Booking(
            customer_name=data['customer_name'],
            check_in=check_in_date,
            check_out=check_out_date,
            room_id=room_id,         # Associa la prenotazione alla stanza
            user_id=current_user_id  # Associa la prenotazione all'utente autenticato
        )
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@bookings_bp.route('/bookings/<int:id>', methods=['PATCH'])
@jwt_required()
def update_booking(id: int):
    booking = Booking.query.get_or_404(id)
    data = request.get_json()

    if 'customer_name' in data:
        booking.customer_name = data['customer_name']
    if 'check_in' in data:
        try:
            booking.check_in = datetime.strptime(data['check_in'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format for check_in. Use YYYY-MM-DD'}), 400
    if 'check_out' in data:
        try:
            booking.check_out = datetime.strptime(data['check_out'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format for check_out. Use YYYY-MM-DD'}), 400
    if 'room_id' in data:
        # Verifica se la stanza è già prenotata per le nuove date
        room_id = data['room_id']
        conflicting_booking = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.id != id,
            Booking.check_in < booking.check_out,
            Booking.check_out > booking.check_in
        ).first()

        if conflicting_booking:
            return jsonify({'message': 'Room is already booked for the selected dates'}), 400

        booking.room_id = room_id

    db.session.commit()
    return jsonify({'message': 'Booking updated successfully', 'booking': booking.to_dict()}), 200


@bookings_bp.route('/bookings/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(id: int):
    booking = Booking.query.get_or_404(id)

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted, room is now available'})


@bookings_bp.route('/bookings/user', methods=['GET'])
@jwt_required()
def get_user_bookings():
    try:
        current_user_id = get_jwt_identity()  # ID dell'utente autenticato

        user_bookings = Booking.query.filter_by(user_id=current_user_id).all()  # Recupera le prenotazioni dell'utente

        result = [booking.to_dict() for booking in user_bookings]
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
