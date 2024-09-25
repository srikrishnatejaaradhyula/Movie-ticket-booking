from flask import request, jsonify
from app import app, db , cache
from app.token import token_required
from app.model import Show, Venue, Booking , UserAuth
from datetime import datetime
from app.mail import send_email


@app.route('/api/create_show', methods=['POST'])
@token_required
def create_show():
    data = request.get_json()
    name = data['name']
    starting_time = data['starting_time']
    ending_time = data['ending_time']
    tag = data['tag']
    price = data['price']
    rating = data['rating']
    venue_id = data['venue_id']
    
    venue = Venue.query.filter_by(id=venue_id).first()

    py_starting_time = starting_time.replace('T', '-')
    py_ending_time = ending_time.replace('T', '-')

    py_starting_time += ':00'
    py_ending_time += ':00'

    py_starting_time = datetime.strptime(py_starting_time, '%Y-%m-%d-%H:%M:%S')
    py_ending_time = datetime.strptime(py_ending_time, '%Y-%m-%d-%H:%M:%S')

    

    show = Show(venue_id=venue_id, 
                name=name, 
                starting_time=py_starting_time, 
                ending_time=py_ending_time, 
                tag=tag, 
                price=price,
                rating=rating,
                available_seats=venue.capacity)
    db.session.add(show)
    db.session.commit()
    return jsonify({'success': True}), 200


@app.route('/api/get_show', methods=['GET', 'POST'])
@token_required
def get_show():
    data = request.get_json()
    venue_id = data['venue_id']

    #cache
    # cache_key = f'show_data_{venue_id}'
    
    # cached_data = cache.get(cache_key)
    # if cached_data is not None:
    #     return jsonify(cached_data)
    
    
    if venue_id is  None:
        return jsonify({'error': 'Venue id not found'}), 500
    else:
        show = Show.query.filter_by(venue_id=venue_id).all()
        show_data = []
        for s in show:
            start_date = datetime.strptime(str(s.starting_time), '%Y-%m-%d %H:%M:%S')
            end_date = datetime.strptime(str(s.ending_time), '%Y-%m-%d %H:%M:%S')
            common_date, time_range = separate_date_time(start_date, end_date)
            show_data.append({
                'id': s.id,
                'name': s.name,
                'starting_time': s.starting_time,
                'ending_time': s.ending_time,
                'common_date': common_date,
                'time_range': time_range,
                'tag': s.tag,
                'price': s.price,
                'rating': s.rating,
                'available_seats': s.available_seats
            })
        #cache
        # cache.set(cache_key, show_data, timeout=5*60)
        return jsonify(show_data)


def separate_date_time(start_date, end_date):
    common_date_part = start_date.strftime('%a, %d %b %Y')

    start_time = start_date.strftime('%H:%M:%S')
    end_time = end_date.strftime('%H:%M:%S')
    time_range = f"{start_time} - {end_time}"

    return common_date_part, time_range


@app.route('/api/get_show_by_id', methods=['GET', 'POST'])
@token_required
def get_show_by_id():
    data = request.get_json()
    show_id = data['show_id']
    #cache
    # cache_key = f'show_data_by_id_{show_id}'
    # cached_data = cache.get(cache_key)
    # if cached_data is not None:
    #     return jsonify(cached_data)
    
    show = Show.query.filter_by(id=show_id).first()
    start_date = datetime.strptime(str(show.starting_time), '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(str(show.ending_time), '%Y-%m-%d %H:%M:%S')
    show_data = {
        'id': show.id,
        'name': show.name,
        'starting_time': show.starting_time,
        'ending_time': show.ending_time,
        'tag': show.tag,
        'price': show.price,
        'rating': show.rating,
        'available_seats': show.available_seats
    }
    #cache
    # cache.set(cache_key, show_data, timeout=5*60)
    return jsonify(show_data)
   

@app.route('/api/get_show_all', methods=['GET', 'POST'])
@token_required
def get_show_all():
    #cache
    cache_key = f'show_data_all'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    
    show = Show.query.all()
    show_data = []
    current_date = datetime.now()
    for s in show:
        start_date = datetime.strptime(str(s.starting_time), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(str(s.ending_time), '%Y-%m-%d %H:%M:%S')
        if current_date > end_date:
            viewable = False
        else:
            viewable = True
        common_date, time_range = separate_date_time(start_date, end_date)
        venue = Venue.query.filter_by(id=s.venue_id).first()
        show_data.append({
            'id': s.id,
            'name': s.name,
            'starting_time': s.starting_time,
            'ending_time': s.ending_time,
            'common_date': common_date,
            'time_range': time_range,
            'tag': s.tag,
            'price': s.price,
            'rating': s.rating,
            'available_seats': s.available_seats,
            'venue_id': s.venue_id,
            'venue_name': venue.name,
            'venue_address': venue.location+','+venue.place,
            'viewable': viewable
        })
    #cache
    cache.set(cache_key, show_data, timeout=5*60)
    return jsonify(show_data)


@app.route('/api/update_show', methods=['GET', 'POST'])
@token_required
def update_show():
    data = request.get_json()
    show_id = data['show_id']
    starting_time = data['starting_time']
    ending_time = data['ending_time']
    show = Show.query.filter_by(id=show_id).first()
    if show is None:
        return jsonify({'error': 'Show not found'}), 400
    
    py_starting_time = starting_time.replace('T', '-')
    py_ending_time = ending_time.replace('T', '-')

    py_starting_time += ':00'
    py_ending_time += ':00'

    py_starting_time = datetime.strptime(py_starting_time, '%Y-%m-%d-%H:%M:%S')
    py_ending_time = datetime.strptime(py_ending_time, '%Y-%m-%d-%H:%M:%S')

    show.name = data['name']
    show.starting_time = py_starting_time
    show.ending_time = py_ending_time
    show.tag = data['tag']
    show.price = data['price']
    show.rating = data['rating']
    # cache.delete('show_data_'+str(show.venue_id))
    # cache.delete('show_data_by_id_'+str(show_id))
    booking = Booking.query.filter_by(show_id=show_id).all()
    current = datetime.now()
    book = False
    start_date = datetime.strptime(str(show.starting_time), '%Y-%m-%d %H:%M:%S')
    if current < start_date:
        for b in booking:
            user = UserAuth.query.filter_by(id=b.user_id).first()
            send_email("mad2project.ticketshow@gmail.com",user.email, 'Update', f'There are some modification in show which is already booked by you.\nPlease visit the page for more details.\nThank You.\n \n \n Please contact us for further details.')
            book = True
    cache.delete('show_data_all')
    cache.delete('show_data_summery')
    db.session.commit()
    return jsonify({'success': True,'book':book}), 200


@app.route('/api/delete_show', methods=['GET', 'POST'])
@token_required
def delete_show():
    data = request.get_json()
    show_id = data['show_id']
    show = Show.query.filter_by(id=show_id).first()
    if show is None:
        return jsonify({'error': 'Show not found'}), 400
    booking = Booking.query.filter_by(show_id=show_id).all()
    current = datetime.now()
    start_date = datetime.strptime(str(show.starting_time), '%Y-%m-%d %H:%M:%S')
    if current < start_date:
        for b in booking:
            user = UserAuth.query.filter_by(id=b.user_id).first()
            send_email("mad2project.ticketshow@gmail.com",user.email, 'Booking Cancelled', f'Your booking for {show.name} has been cancelled.\n your money will be Refunded \n Please contact us for further details.')
            db.session.delete(b)
    #cache
    # cache.delete('show_data_'+str(show.venue_id))
    # cache.delete('show_data_by_id_'+str(show_id))
    cache.delete('show_data_all')
    cache.delete('show_data_summery')
    db.session.delete(show)
    db.session.commit()
    return jsonify({'success': True}), 200


@app.route('/api/get_show_for_summery', methods=['GET', 'POST'])
@token_required
def get_show_for_summery():
    #cache
    cache_key = f'show_data_summery'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    show = Show.query.all()
    show_data = []
    for s in show:
        booking = Booking.query.filter_by(show_id=s.id).all()
        # venues = Venue.query.filter_by(id=s.venue_id).first()
        revenue = 0
        for b in booking:
            revenue = revenue + b.total_price
        if len(booking) == 0:
            continue
        show_data.append({
            'id': s.id,
            'name': s.name,
            'admin_rating' : s.rating,
            'user_rating' : sum([b.rating for b in booking])/len(booking),
            'booking_count' : sum([b.seats for b in booking]),
            'Unoccupied_seats' : s.available_seats,
            'revenue' : revenue
        })
    #cache
    cache.set(cache_key, show_data, timeout=5*60)
    return jsonify(show_data)


