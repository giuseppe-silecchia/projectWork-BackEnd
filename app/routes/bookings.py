from flask import Blueprint, jsonify, request
from ..models import Booking, Room
from .. import db
from datetime import datetime

bookings_bp = Blueprint('bookings_bp', __name__)


@bookings_bp.route('/bookings', methods=['GET'])
def get_bookings():
    try:
        bookings = Booking.query.all()
        result = [booking.to_dict() for booking in bookings]
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@bookings_bp.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id: int):
    booking = Booking.query.get_or_404(id)
    result = booking.to_dict()
    return jsonify(result)


@bookings_bp.route('/bookings', methods=['POST'])
def create_booking():
    try:

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
            room_id=room_id
        )
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@bookings_bp.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id: int):
    booking = Booking.query.get_or_404(id)

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted, room is now available'})
