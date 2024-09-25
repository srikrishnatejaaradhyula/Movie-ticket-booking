from flask import request, jsonify
from app import app, db, cache
from app.token import token_required
from app.model import Venue, Show, Booking


@app.route('/api/create_venue', methods=['POST'])
@token_required
def create_post():
    data = request.get_json()
    name = data['name']
    place = data['place']
    location = data['location']
    capacity = data['capacity']
    admin_id = data['admin_id']

    venue = Venue(admin_id=admin_id, name=name, place=place, location=location, capacity=capacity)
    db.session.add(venue)
    db.session.commit()
    cache.delete('venue_data')
    cache.delete('venue_data_by_id')
    cache.delete('venue_data_all')
    return jsonify({'success': True}), 200


@app.route('/api/get_venue', methods=['GET', 'POST'])
@token_required
def get_venue():
    data = request.get_json()
    admin_id = data['admin_id']
    #cache
    cache_key = f'venue_data'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    
    venue = Venue.query.filter_by(admin_id=admin_id).all()
    venue_data = []
    for v in venue:
        venue_data.append({
            'id': v.id,
            'name': v.name,
            'place': v.place,
            'location': v.location,
            'capacity': v.capacity
        })
    #cache
    cache.set(cache_key, venue_data, timeout=5*60)
    return jsonify(venue_data)


@app.route('/api/get_all_venue', methods=['GET', 'POST'])
@token_required
def get_all_venue():
    #cache
    cache_key = f'venue_data_all'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    
    venue = Venue.query.all()
    venue_data = []
    for v in venue:
        venue_data.append({
            'id': v.id,
            'name': v.name,
            'place': v.place,
            'location': v.location,
            'capacity': v.capacity
        })
    #cache
    cache.set(cache_key, venue_data, timeout=5*60)
    return jsonify(venue_data)

@app.route('/api/get_venue_by_id', methods=['GET', 'POST'])
@token_required
def get_venue_by_id():
    data = request.get_json()
    #cache
    cache_key = f'venue_data_by_id'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return jsonify(cached_data)
    venue_id = data['venue_id']
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue is None:
        return jsonify({'error': 'Venue not found'}), 400
    venue_data = {
        'id': venue.id,
        'name': venue.name,
        'place': venue.place,
        'location': venue.location,
        'capacity': venue.capacity
    }
    #cache
    cache.set(cache_key, venue_data, timeout=5*60)
    return jsonify(venue_data)


@app.route('/api/update_venue', methods=['GET', 'POST'])
@token_required
def update_venue():
    data = request.get_json()
    venue_id = data['venue_id']
    venue = Venue.query.filter_by(id=venue_id).first()
    if venue is None:
        return jsonify({'error': 'Venue not found'}), 400
    show = Show.query.filter_by(venue_id=venue_id).all()
    if show is not None:
        for s in show:
            booking = Booking.query.filter_by(show_id=s.id).all()
            if booking is not None:
                count = 0
                for b in booking:
                    count = count + b.seats 
                s.available_seats = data['capacity'] - count
            else:
                s.available_seats = data['capacity']

    venue.name = data['name']
    venue.place = data['place']
    venue.location = data['location']
    venue.capacity = data['capacity']
    #cache
    cache.delete('venue_data')
    cache.delete('venue_data_by_id')
    cache.delete('venue_data_all')
    db.session.commit()
    return jsonify({'success': True}), 200



@app.route('/api/delete_venue', methods=['GET', 'POST'])
@token_required
def delete_venue():
    data = request.get_json()
    venue_id = data['venue_id']
    venue = Venue.query.filter_by(id=venue_id).first()
    show = Show.query.filter_by(venue_id=venue_id).all()
    if venue is None:
        return jsonify({'error': 'Venue not found'}), 400
    if show is not None:
        for s in show:
            booking = Booking.query.filter_by(show_id=s.id).all()
            if booking is not None:
                for b in booking:
                    db.session.delete(b)
            db.session.delete(s)
    #cache
    cache.delete('venue_data')
    cache.delete('venue_data_by_id')
    cache.delete('venue_data_all')
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'success': True}), 200

@app.route('/api/get_venue_for_summery', methods=['GET', 'POST'])
@token_required
def get_venue_for_summery():
    booking = Booking.query.all()
    venue = Venue.query.all()
    venue_data = []
    venue_name = []
    profit = []
    for v in venue:
        venue_name.append(v.name)
        show = Show.query.filter_by(venue_id=v.id).all()
        total_profit = 0
        for s in show:
            for b in booking:
                if b.show_id == s.id:
                    total_profit = total_profit + b.total_price
        profit.append(total_profit) 
    venue_data.append({
        'venue_name': venue_name,
        'revenue': profit
    })
    return jsonify(venue_data)


