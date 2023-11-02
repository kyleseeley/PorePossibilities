from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime


class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    staffId = db.Column(db.Integer, db.ForeignKey(
        add_prefix_for_prod('staffs.id')), nullable=False)
    title = db.Column(db.String(), nullable=False)
    blog = db.Column(db.String(), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    staff = db.relationship("Staff", back_populates="blogpost")

    def to_dict(self):
        return {
            'id': self.id,
            'staffId': self.staffId,
            'title': self.title,
            'blog': self.blog
        }