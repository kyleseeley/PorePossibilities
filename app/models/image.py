from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Image(db.Model):
    __tablename__ = 'images'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    imageFile = db.Column(db.String(255), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'imageFile': self.imageFile
        }
