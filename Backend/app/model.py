from app import db


class UserAuth(db.Model):
    __tablename__ = 'userauth'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class AdminAuth(db.Model):
    __tablename__ = 'adminauth'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_login = db.Column(db.DateTime)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('adminauth.id' , onupdate='CASCADE', ondelete='CASCADE'), nullable=False)


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    starting_time = db.Column(db.DateTime, nullable=False)
    ending_time = db.Column(db.DateTime, nullable=False)
    tag = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seats = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    booking_time = db.Column(db.DateTime, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('userauth.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
