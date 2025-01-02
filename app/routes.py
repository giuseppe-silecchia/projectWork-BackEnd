from flask import Blueprint, jsonify, request
from . import db
from .models import Room, Booking
from datetime import datetime

# creazione di un oggetto Blueprint di nome main che appartiene al modulo corrente
main = Blueprint('main', __name__)


@main.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    result = [
        room.to_dict()
        for room in rooms
    ]
    return jsonify(result)


@main.route('/rooms/<int:id>', methods=['GET'])
def get_room(id: int):
    room = Room.query.get_or_404(id)
    result = room.to_dict()
    return jsonify(result)


@main.route('/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    new_room = Room(
        room_number=data['room_number'],
        max_people=data['max_people']
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully'}), 201

@main.route('/rooms/<int:id>', methods=['DELETE'])
def delete_room(id: int):
    room = Room.query.get_or_404(id)

    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted'})

@main.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    result = [booking.to_dict() for booking in bookings]
    return jsonify(result)


@main.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id: int):
    booking = Booking.query.get_or_404(id)
    result = booking.to_dict()
    return jsonify(result)

@main.route('/bookings', methods=['POST'])
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


@main.route('/bookings/<int:id>', methods=['DELETE'])
def cancel_booking(id: int):
    booking = Booking.query.get_or_404(id)

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted, room is now available'})


@main.route('/rooms/available', methods=['GET'])
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

    available_rooms = Room.query.filter(~Room.id.in_(unavailable_rooms)).all()

    result = [room.to_dict() for room in available_rooms]

    return jsonify(result)
