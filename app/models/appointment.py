from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    serviceId = db.Column(db.Integer(), db.ForeignKey(add_prefix_for_prod('services.id')), nullable=False)
    staffId = db.Column(db.Integer(), db.ForeignKey(add_prefix_for_prod('staffs.id')), nullable=False)
    appointmentDate = db.Column(db.Date, nullable=False)
    appointmentTime = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(), nullable=False)

    user = db.relationship('User', back_populates='appointments', cascade="all, delete-orphan")

    services = db.relationship('Service', back_populates='appointment')

    staff = db.relationship('Staff', back_populates='appointments')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'serviceId': self.serviceId,
            'staffId': self.staffId,
            'appointmentDate': self.appointmentDate,
            'appointmentTime': self.appointmentTime,
            'status': self.status
        }