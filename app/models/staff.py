from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Staff(db.Model):
    __tablename__ = 'staffs'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    availability = db.Column(db.JSON(), nullable=False)
    authorized = db.Column(db.BOOLEAN(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = db.relationship('Appointment', back_populates='staff')

    blogpost = db.relationship("BlogPost", back_populates="staff")

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'availability': self.availability
        }
