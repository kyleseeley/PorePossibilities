from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')))
    serviceId = db.Column(db.Integer(), db.ForeignKey(add_prefix_for_prod('services.id')), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)

    user = db.relationship('User', back_populates='cart', cascade="all, delete-orphan")

    services = db.relationship('Service', back_populates='cart')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'serviceId': self.serviceId,
            'quantiy': self.quantity
        }
