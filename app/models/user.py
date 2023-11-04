from .db import db, environment, SCHEMA
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(35), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = db.relationship(
        'Appointment', back_populates='user', cascade="all, delete-orphan")

    reviews = db.relationship(
        'Review', back_populates='user', cascade="all, delete-orphan")

    cart = db.relationship('Cart', back_populates='user')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
            'username': self.username,
            'address': self.address,
            'city': self.city,
            'state': self.state,
        }

    def get_cart(self):
        if self.cart:
            return [{
                'cart': cart.to_dict()
            } for cart in self.cart]
        else:
            return None

    def get_reviews(self):
        return {
            'reviews': [review.to_dict() for review in self.reviews]
        }

    def get_appointments(self):
        return {
            'appointments': [appointment.to_dict() for appointment in self.appointments]
        }
