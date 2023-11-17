from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Cart(db.Model):
    __tablename__ = 'carts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')))
    companyId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('companies.id')))
    cartTotal = db.Column(db.Integer(), default=0, nullable=False)
    checkedOut = db.Column(db.Boolean, default=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    user = db.relationship('User', back_populates='cart')

    company = db.relationship('Company', back_populates='cart')

    cart_items = db.relationship(
        'CartItem', back_populates='cart', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'companyId': self.companyId,
            'cartTotal': self.calculate_cart_total(),
            'checkedOut': self.checkedOut
        }

    def calculate_cart_total(self):
        total = 0
        for item in self.cart_items:
            total += item.serviceTotal
        return total
