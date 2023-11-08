from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError


def employee_data(form, field):
    employeeId = field.data
    if not employeeId:
        raise ValidationError(
            "Please select the employee you would like")


def appointmentDate_data(form, field):
    appointmentDate = field.data
    if not appointmentDate:
        raise ValidationError(
            "Please select the date you would like")


def appointmentTime_data(form, field):
    appointmentTime = field.data
    if not appointmentTime:
        raise ValidationError(
            "Please select the time you would like")


class AppointmentForm(FlaskForm):
    employeeId = IntegerField('Employee', validators=[DataRequired()])
    appointmentDate = DateField('Date', validators=[DataRequired()])
    appointmentTime = SelectField('Time', validators=[DataRequired()], choices=[
        '9:00 AM', '9:15 AM', '9:30 AM', '9:45 AM', '10:00 AM',
        '10:15 AM', '10:30 AM', '10:45 AM', '11:00 AM', '11:15 AM',
        '11:30 AM', '11:45 AM', '12:00 PM', '12:15 PM', '12:30 PM',
        '12:45 PM', '1:00 PM', '1:15 PM', '1:30 PM', '1:45 PM',
        '2:00 PM', '2:15 PM', '2:30 PM', '2:45 PM', '3:00 PM',
        '3:15 PM', '3:30 PM', '3:45 PM', '4:00 PM', '4:15 PM',
        '4:30 PM', '4:45 PM', '5:00 PM', '5:15 PM', '5:30 PM'
    ])
