from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Service(db.Model):
    __tablename__ = 'services'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    appointmentId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('appointments.id')))
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    appointment = db.relationship(
        'Appointment', back_populates='services')

    cart_items = db.relationship('CartItem', back_populates='service')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }

    def get_appointments(self):
        if self.appointment:
            return [appointment.to_dict() for appointment in self.appointment]
        else:
            return []

    def get_cart_items(self):
        if self.cart_items:
            return [cart_item.to_dict() for cart_item in self.cart_items]
        else:
            return []
