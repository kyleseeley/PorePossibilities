from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Staff(db.Model):
    __tablename__ = 'staffs'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    authorized = db.Column(db.BOOLEAN(), nullable=False)
    availability = db.Column(db.JSON(), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    is_owner = db.Column(db.Boolean, nullable=False, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = db.relationship('Appointment', back_populates='staff')

    blogpost = db.relationship("BlogPost", back_populates="staff")

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
            'availability': self.availability,
            'is_owner': self.is_owner
        }
