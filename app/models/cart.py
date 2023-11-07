from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Cart(db.Model):
    __tablename__ = 'carts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')))
    companyId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('companies.id')))
    serviceId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('services.id')))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='cart')

    company = db.relationship('Company', back_populates='cart')

    cart_items = db.relationship('CartItem', back_populates='cart')

    services = db.relationship('Service', back_populates='cart')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'companyId': self.companyId,
            'cartTotal': self.calculate_cart_total()
        }

    def calculate_cart_total(self):
        total = 0
        for item in self.cart_items:
            total += item.serviceTotal
        return total
