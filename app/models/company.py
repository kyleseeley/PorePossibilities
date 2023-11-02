from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Company(db.Model):
    __tablename__ = 'companies'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    ownerId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('staffs.id')), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(35), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zipCode = db.Column(db.String(5), nullable=False)
    starRating = db.Column(db.Float())
    numReviews = db.Column(db.Integer())
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship("Staff", back_populates='companies')

    reviews = db.relationship('Review', back_populates='company')

    def to_dict(self):
        return {
            'id': self.id,
            'ownerId': self.ownerId,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'starRating': self.starRating,
            'numReviews': self.numReviews
        }

    def get_reviews(self):
        return {
            'reviews': [review.to_dict() for review in self.reviews]
        }