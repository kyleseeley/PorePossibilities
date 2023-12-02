from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
import pytz


mountain_timezone = pytz.timezone('US/Mountain')


class Appointment(db.Model):
    __tablename__ = 'appointments'

    if environment == 'production':
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('users.id')), nullable=False)
    companyId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('companies.id')))
    employeeId = db.Column(db.Integer(), db.ForeignKey(
        add_prefix_for_prod('employees.id')), nullable=False)
    appointmentDate = db.Column(db.Date, nullable=False)
    appointmentTime = db.Column(db.Time, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now(mountain_timezone))
    updatedAt = db.Column(
        db.DateTime, default=datetime.now(mountain_timezone), onupdate=datetime.now(mountain_timezone))

    user = db.relationship(
        'User', back_populates='appointments')

    services = db.relationship(
        'Service', back_populates='appointment')

    employee = db.relationship('Employee', back_populates='appointments')

    company = db.relationship('Company', back_populates='appointments')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'companyId': self.companyId,
            'employeeId': self.employeeId,
            'appointmentDate': self.appointmentDate.strftime('%b %d, %Y'),
            'appointmentTime': self.appointmentTime.strftime('%I:%M %p').lstrip('0'),
            'services': [service.to_dict() for service in self.services],
            'employee': self.employee.to_dict() if self.employee else None
        }

    @property
    def appointmentTimeStr(self):
        return self.appointmentTime.strftime('%I:%M %p')

    @appointmentTimeStr.setter
    def appointmentTimeStr(self, value):
        self.appointmentTime = datetime.strptime(value, '%I:%M %p').time()
