from .db import db, environment, SCHEMA, add_prefix_for_prod


class CartItem(db.Model):
    __tablename__ = 'cartitems'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    cartId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('carts.id')), nullable=False)
    serviceId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('services.id')), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    serviceTotal = db.Column(db.Integer(), nullable=False)

    cart = db.relationship('Cart', back_populates='cart_items')
    
    service = db.relationship('Service', back_populates='cart_items')

    def to_dict(self):
        return {
            'id': self.id,
            'cartId': self.cartId,
            'serviceId': self.serviceId,
            'quantity': self.quantity,
            'price': self.price,
            'serviceTotal': self.serviceTotal
        }
