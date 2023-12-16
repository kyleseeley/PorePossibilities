from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Company(db.Model):
    __tablename__ = 'companies'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    ownerId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('employees.id')), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(35), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zipCode = db.Column(db.String(5), nullable=False)
    starRating = db.Column(db.Float())
    numReviews = db.Column(db.Integer())
    monday_open = db.Column(db.Time())
    monday_close = db.Column(db.Time())
    tuesday_open = db.Column(db.Time())
    tuesday_close = db.Column(db.Time())
    wednesday_open = db.Column(db.Time())
    wednesday_close = db.Column(db.Time())
    thursday_open = db.Column(db.Time())
    thursday_close = db.Column(db.Time())
    friday_open = db.Column(db.Time())
    friday_close = db.Column(db.Time())
    saturday_open = db.Column(db.Time())
    saturday_close = db.Column(db.Time())
    sunday_open = db.Column(db.Time())
    sunday_close = db.Column(db.Time())
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    owner = db.relationship("Employee", back_populates='companies')

    reviews = db.relationship(
        'Review', back_populates='company', cascade="all, delete-orphan")

    cart = db.relationship('Cart', back_populates='company')

    appointments = db.relationship('Appointment', back_populates='company')

    def to_dict(self):
        return {
            'id': self.id,
            'ownerId': self.ownerId,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'starRating': self.starRating,
            'numReviews': self.numReviews,
            'monday_open': str(self.monday_open) if self.monday_open else None,
            'monday_close': str(self.monday_close) if self.monday_close else None,
            'tuesday_open': str(self.tuesday_open) if self.tuesday_open else None,
            'tuesday_close': str(self.tuesday_close) if self.tuesday_close else None,
            'wednesday_open': str(self.wednesday_open) if self.wednesday_open else None,
            'wednesday_close': str(self.wednesday_close) if self.wednesday_close else None,
            'thursday_open': str(self.thursday_open) if self.thursday_open else None,
            'thursday_close': str(self.thursday_close) if self.thursday_close else None,
            'friday_open': str(self.friday_open) if self.friday_open else None,
            'friday_close': str(self.friday_close) if self.friday_close else None,
            'saturday_open': str(self.saturday_open) if self.saturday_open else None,
            'saturday_close': str(self.saturday_close) if self.saturday_close else None,
            'sunday_open': str(self.sunday_open) if self.sunday_open else None,
            'sunday_close': str(self.sunday_close) if self.sunday_close else None,
        }

    def get_reviews(self):
        return {
            'reviews': [review.to_dict() for review in self.reviews]
        }

    def get_appointments(self):
        return {
            'appointments': [appointment.to_dict() for appointment in self.appointments]
        }
