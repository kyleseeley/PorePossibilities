from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Review(db.Model):
    __tablename__ = 'reviews'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')))
    companyId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('companies.id')))
    review = db.Column(db.String(), nullable=False)
    stars = db.Column(db.Integer(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    user = db.relationship('User', back_populates='reviews')

    company = db.relationship(
        'Company', back_populates='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'companyId': self.companyId,
            'review': self.review,
            'stars': self.stars,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'createdAt': self.createdAt.astimezone(mountain_timezone).strftime('%a, %d %b %Y %H:%M:%S %Z'),
            'updatedAt': self.updatedAt.astimezone(mountain_timezone).strftime('%a, %d %b %Y %H:%M:%S %Z') if self.updatedAt else None
        }
