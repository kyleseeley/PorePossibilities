from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    authorized = db.Column(db.BOOLEAN(), nullable=False)
    monday_start = db.Column(db.Time)
    monday_end = db.Column(db.Time)
    tuesday_start = db.Column(db.Time)
    tuesday_end = db.Column(db.Time)
    wednesday_start = db.Column(db.Time)
    wednesday_end = db.Column(db.Time)
    thursday_start = db.Column(db.Time)
    thursday_end = db.Column(db.Time)
    friday_start = db.Column(db.Time)
    friday_end = db.Column(db.Time)
    saturday_start = db.Column(db.Time)
    saturday_end = db.Column(db.Time)
    sunday_start = db.Column(db.Time)
    sunday_end = db.Column(db.Time)
    hashed_password = db.Column(db.String(255), nullable=False)
    is_owner = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = db.relationship('Appointment', back_populates='employee')

    blogpost = db.relationship("BlogPost", back_populates="employee")

    companies = db.relationship("Company", back_populates='owner')

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
            'authorized': self.authorized,
            'monday_start': self.monday_start.strftime('%I:%M %p') if self.monday_start else None,
            'monday_end': self.monday_end.strftime('%I:%M %p') if self.monday_end else None,
            'tuesday_start': self.tuesday_start.strftime('%I:%M %p') if self.tuesday_start else None,
            'tuesday_end': self.tuesday_end.strftime('%I:%M %p') if self.tuesday_end else None,
            'wednesday_start': self.wednesday_start.strftime('%I:%M %p') if self.wednesday_start else None,
            'wednesday_end': self.wednesday_end.strftime('%I:%M %p') if self.wednesday_end else None,
            'thursday_start': self.thursday_start.strftime('%I:%M %p') if self.thursday_start else None,
            'thursday_end': self.thursday_end.strftime('%I:%M %p') if self.thursday_end else None,
            'friday_start': self.friday_start.strftime('%I:%M %p') if self.friday_start else None,
            'friday_end': self.friday_end.strftime('%I:%M %p') if self.friday_end else None,
            'saturday_start': self.saturday_start.strftime('%I:%M %p') if self.saturday_start else None,
            'saturday_end': self.saturday_end.strftime('%I:%M %p') if self.saturday_end else None,
            'sunday_start': self.sunday_start.strftime('%I:%M %p') if self.sunday_start else None,
            'sunday_end': self.sunday_end.strftime('%I:%M %p') if self.sunday_end else None,
            'is_owner': self.is_owner
        }
