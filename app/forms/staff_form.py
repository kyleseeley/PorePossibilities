from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SelectField, FloatField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import Staff


def staff_exists(form, field):
    # Checking if user exists
    email = field.data
    if current_user.is_authenticated and current_user.email == email:
        staff = Staff.query.filter(Staff.email == email).all()
        if len(staff) > 1:
            raise ValidationError('Email address is already in use.')
    else:
        staff = Staff.query.filter(Staff.email == email).first()
        if staff:
            raise ValidationError('Email address is already in use.')


def firstname_data(form, field):
    firstname = field.data
    if len(firstname) < 2:
        raise ValidationError(
            "Please enter in a first name with at least 2 characters")


def lastname_data(form, field):
    lastname = field.data
    if len(lastname) < 2:
        raise ValidationError(
            "Please enter in a last name with at least 2 characters")


def authorized_data(form, field):
    authorized = field.data
    if not authorized:
        raise ValidationError("Please select a value for authorized")


class StaffForm(FlaskForm):
    time_slots = [
        '9:00 AM', '9:15 AM', '9:30 AM', '9:45 AM', '10:00 AM',
        '10:15 AM', '10:30 AM', '10:45 AM', '11:00 AM', '11:15 AM',
        '11:30 AM', '11:45 AM', '12:00 PM', '12:15 PM', '12:30 PM',
        '12:45 PM', '1:00 PM', '1:15 PM', '1:30 PM', '1:45 PM',
        '2:00 PM', '2:15 PM', '2:30 PM', '2:45 PM', '3:00 PM',
        '3:15 PM', '3:30 PM', '3:45 PM', '4:00 PM', '4:15 PM',
        '4:30 PM', '4:45 PM', '5:00 PM', '5:15 PM', '5:30 PM',
        '5:45 PM', '6:00 PM'
    ]

    firstname = StringField('First Name', validators=[
                            DataRequired(), firstname_data, Length(min=2)])
    lastname = StringField('Last Name', validators=[
                           DataRequired(), lastname_data, Length(min=2)])
    email = EmailField('Email', validators=[DataRequired(), staff_exists])
    authorized = SelectField('Authorized', validators=[
                             DataRequired(), authorized_data], choices=['True', 'False'])
    monday_availability = SelectField(
        'Monday Availability', choices=time_slots)
    tuesday_availability = SelectField(
        'Tuesday Availability', choices=time_slots)
    wednesday_availability = SelectField(
        'Wednesday Availability', choices=time_slots)
    thursday_availability = SelectField(
        'Thursday Availability', choices=time_slots)
    friday_availability = SelectField(
        'Friday Availability', choices=time_slots)
    saturday_availability = SelectField(
        'Saturday Availability', choices=time_slots)
    sunday_availability = SelectField(
        'Sunday Availability', choices=time_slots)
