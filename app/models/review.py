from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class Review(db.Model):
    __tablename__ = 'reviews'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')))
    review = db.Column(db.String(), nullable=False)
    stars = db.Column(db.Integer(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='reviews', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'review': self.review,
            'stars': self.stars,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }