from flask import Blueprint, jsonify, request
from sqlalchemy import not_
from ..models import Room, Booking
from .. import db
from datetime import datetime

rooms_bp = Blueprint('rooms_bp', __name__)


@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = Room.query.all()
        result = [
            room.to_dict()
            for room in rooms
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@rooms_bp.route('/rooms/<int:id>', methods=['GET'])
def get_room(id: int):
    room = Room.query.get_or_404(id)
    result = room.to_dict()
    return jsonify(result)


@rooms_bp.route('/rooms', methods=['POST'])
def add_room():
    try:
        data = request.get_json()
        if 'room_number' not in data or 'max_people' not in data:
            return jsonify({'message': 'room_number and max_people are required'}), 400

        new_room = Room(
            room_number=data['room_number'],
            max_people=data['max_people']
        )
        db.session.add(new_room)
        db.session.commit()
        return jsonify({'message': 'Room added successfully'}), 201
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@rooms_bp.route('/rooms/<int:id>', methods=['PATCH'])
def update_room(id: int):
    room = Room.query.get_or_404(id)
    data = request.get_json()

    if 'room_number' in data:
        room.room_number = data['room_number']
    if 'max_people' in data:
        room.max_people = data['max_people']

    db.session.commit()
    return jsonify({'message': 'Room updated successfully', 'room': room.to_dict()}), 200
    

@rooms_bp.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id: int):
    room = Room.query.get_or_404(id)

    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted'})


@rooms_bp.route('/rooms/available', methods=['GET'])
def get_available_rooms():
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')

    if not check_in or not check_out:
        return jsonify({'message': 'Check-in and check-out dates are required'}), 400

    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if check_in_date >= check_out_date:
        return jsonify({'message': 'Check-out date must be after check-in date'}), 400

    # Query per ottenere tutte le stanze che NON hanno prenotazioni sovrapposte
    unavailable_rooms = db.session.query(Booking.room_id).filter(
        Booking.check_in < check_out_date,
        Booking.check_out > check_in_date
    ).subquery()

    available_rooms = Room.query.filter(not_(Room.id.in_(unavailable_rooms))).all()

    result = [room.to_dict() for room in available_rooms]

    return jsonify(result)
