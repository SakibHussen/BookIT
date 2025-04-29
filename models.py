from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()
class User(db.Model):
    __tablename__='user' # This specify the table name in database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(255),unique=True, nullable= False)
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    admin = db.Column(db.Boolean, default=False, nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True) # create one to many relationship, where a user can have a multiple relationships

    # Flask-Login required attributes
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
# We need a table for event so that when user log in to their site they can see all the available rvent
class Event(db.Model):
    __tablename__ = 'event'
    eventid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    remaining_tickets = db.Column(db.Integer, nullable=False)  # New field for remaining tickets
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    bookings = db.relationship('Booking', backref='event', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        db.CheckConstraint("type IN ('conference', 'concert', 'seminar', 'workshop')", name='check_type'),
        db.CheckConstraint('capacity > 0', name='check_capacity'),
        db.CheckConstraint('cost >= 0', name='check_cost'),
        db.CheckConstraint('start_time >= CURRENT_TIMESTAMP', name='check_start_time'),
        db.CheckConstraint('end_time > start_time', name='check_end_time'),
    )

class Booking(db.Model):
    __tablename__ = 'booking'
    bookingid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_info = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.eventid'), nullable=False)
    
    __table_args__ = (
        db.CheckConstraint("status IN ('confirmed', 'pending', 'canceled')", name='check_status'),
        db.CheckConstraint('quantity > 0', name='check_quantity'),
        db.CheckConstraint('date >= CURRENT_TIMESTAMP', name='check_date'),
    )


