from flask import request, jsonify
from app import app, db, cache
from app.token import token_required
from datetime import datetime
from app.model import Venue, Show, Booking,UserAuth
from app.mail import send_email

@app.route('/api/book_show', methods=['POST'])
@token_required
def book_show():
    data = request.get_json()
    seats = data['seats']
    total_price = data['total_price']
    show_id = data['show_id']
    user_id = data['user_id']
    booking_time = datetime.now()
    booking = Booking(seats=seats, total_price=total_price, show_id=show_id, user_id=user_id, booking_time=booking_time)
    db.session.add(booking)
    show = Show.query.filter_by(id=show_id).first()
    show.available_seats = show.available_seats - seats
    user = UserAuth.query.filter_by(id=user_id).first()
    send_email("mad2project.ticketshow@gmail.com",user.email, 'Booking Confirmation', f'Your booking has been confirmed for {show.name} on {show.starting_time} at {show.venue_id}')
    
    db.session.commit()

    return jsonify({'success': True}), 200


@app.route('/api/get_user_booking', methods=['GET', 'POST'])
@token_required
def get_user_booking():
    data = request.get_json()
    user_id = data['user_id']

    #cache
    cache_key = f'booking_data'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)

    booking = Booking.query.filter_by(user_id=user_id).all()
    booking_data = []
    for b in booking:
        shows = Show.query.filter_by(id=b.show_id).first()
        if shows is None:
            continue
        venue = Venue.query.filter_by(id=shows.venue_id).first()
        start_date = datetime.strptime(str(shows.starting_time), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(str(shows.ending_time), '%Y-%m-%d %H:%M:%S')
        common_date, time_range = separate_date_time(start_date, end_date)
        booking_data.append({
            'id': b.id,
            'seats': b.seats,
            'total_price': b.total_price,
            'show_id': b.show_id,
            'user_id': b.user_id,
            'rating': b.rating,
            'booking_time': b.booking_time,
            'seats_booked' : b.seats,
            'show_name': shows.name,
            'show_date': common_date,
            'show_time': time_range,
            'venue_name': venue.name,
            'venue_location': venue.location,
            'venue_place': venue.place
        })
    cache.set(cache_key, booking_data, timeout=5 * 60)
    return jsonify(booking_data)

def separate_date_time(start_date, end_date):
    common_date_part = start_date.strftime('%a, %d %b %Y')

    start_time = start_date.strftime('%H:%M:%S')
    end_time = end_date.strftime('%H:%M:%S')
    time_range = f"{start_time} - {end_time}"

    return common_date_part, time_range

@app.route('/api/update_rating', methods=['GET', 'POST'])
@token_required
def update_rating():
    data = request.get_json()
    booking_id = data['booking_id']
    rating = data['rating']
    booking = Booking.query.filter_by(id=booking_id).first()
    booking.rating = rating
    #cache
    cache.delete('booking_data')
    cache.delete('booking_data_by_id')

    db.session.commit()
    return jsonify({'success': True}), 200


@app.route('/api/get_user_booking_by_id', methods=['GET', 'POST'])
@token_required
def get_user_booking_by_id():
    data = request.get_json()
    booking_id = data['booking_id']
    #cache
    cache_key = f'booking_data_by_id'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    
    booking = Booking.query.filter_by(id=booking_id).first()
    booking_data = {
        'id': booking.id,
        'seats': booking.seats,
        'total_price': booking.total_price,
        'show_id': booking.show_id,
        'user_id': booking.user_id,
        'rating': booking.rating,
        'booking_time': booking.booking_time,
    }
    cache.set(cache_key, booking_data, timeout=5 * 60)
    return jsonify(booking_data)




