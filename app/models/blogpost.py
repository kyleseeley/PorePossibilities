from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    # employeeId = db.Column(db.Integer, db.ForeignKey(
    #     add_prefix_for_prod('employees.id')), nullable=False)
    title = db.Column(db.String(), nullable=False)
    blog = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    # employee = db.relationship("Employee", back_populates="blogpost")

    def to_dict(self):
        return {
            'id': self.id,
            # 'employeeId': self.employeeId,
            'title': self.title,
            'blog': self.blog
        }
