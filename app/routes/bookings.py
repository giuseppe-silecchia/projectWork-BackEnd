from flask import Blueprint, jsonify, request
from ..models import Booking, Room
from .. import db
from datetime import datetime

bookings_bp = Blueprint('bookings_bp', __name__)

@bookings_bp.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    result = [booking.to_dict() for booking in bookings]
    return jsonify(result)


@bookings_bp.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id: int):
    booking = Booking.query.get_or_404(id)
    result = booking.to_dict()
    return jsonify(result)

@bookings_bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    new_booking = Booking(
        customer_name=data['customer_name'],
        check_in=datetime.strptime(data['check_in'], '%Y-%m-%d'),
        check_out=datetime.strptime(data['check_out'], '%Y-%m-%d'),
        room_id=data['room_id']
    )

    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully'}), 201


@bookings_bp.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id: int):
    booking = Booking.query.get_or_404(id)

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted, room is now available'})