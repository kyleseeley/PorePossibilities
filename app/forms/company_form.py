from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, ValidationError, Optional, Length
import re


def name_data(form, field):
    name = field.data
    if len(name) < 2:
        raise ValidationError(
            "Please enter in a name with at least 2 characters")


def phone_data(form, field):
    phone = field.data
    if not re.match(r'^\d{10}$', phone):
        raise ValidationError("Phone number must be a 10-digit number")


def validate_email(form, field):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
        raise ValidationError("Invalid email address")


def address_data(form, field):
    address = field.data
    if not address:
        raise ValidationError("Please enter in an address")


def city_data(form, field):
    city = field.data
    if not city:
        raise ValidationError("Please enter in an city")


def state_data(form, field):
    state = field.data
    if not state:
        raise ValidationError("Please select a state")


class CompanyForm(FlaskForm):
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

    name = StringField('Name', validators=[
                       DataRequired(), Length(max=50), name_data])
    email = StringField('Email', validators=[DataRequired(), validate_email])
    phone = StringField('Phone', validators=[DataRequired(), phone_data])
    address = StringField('Address', validators=[DataRequired(), address_data])
    city = StringField('City', validators=[DataRequired(), city_data])
    state = SelectField('State', validators=[DataRequired(), state_data], choices=[
        'AL - Alabama', 'AK - Alaska', 'AZ - Arizona', 'AR - Arkansas', 'CA - California', 'CO - Colorado', 'CT - Connecticut', 'DE - Delaware', 'FL - Florida', 'GA - Georgia', 'HI - Hawaii', 'ID - Idaho', 'IL - Illinois', 'IN - Indiana', 'IA - Iowa', 'KS - Kansas', 'KY - Kentucky', 'LA - Louisiana', 'ME - Maine', 'MD - Maryland',
        'MA - Massachusetts', 'MI - Michigan', 'MN - Minnesota', 'MS - Mississippi', 'MO - Missouri', 'MT - Montana', 'NE - Nebraska', 'NV - Nevada', 'NH - New Hampshire', 'NJ - New Jersey',
        'NM - New Mexico', 'NY - New York', 'NC - North Carolina', 'ND - North Dakota', 'OH - Ohio', 'OK - Oklahoma', 'OR - Oregon', 'PA - Pennsylvania', 'RI - Rhode Island', 'SC - South Carolina',
        'SD - South Dakota', 'TN - Tennessee', 'TX - Texas', 'UT - Utah', 'VT - Vermont', 'VA - Virginia', 'WA - Washington', 'WV - West Virginia', 'WI - Wisconsin', 'WY - Wyoming'
    ])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    monday_open = SelectField('Monday Open', validators=[
        Optional()], choices=time_slots)
    monday_close = SelectField('Monday Close', validators=[
        Optional()], choices=time_slots)
    tuesday_open = SelectField('Tuesday Open', validators=[
        Optional()], choices=time_slots)
    tuesday_close = SelectField('Tuesday Close', validators=[
        Optional()], choices=time_slots)
    wednesday_open = SelectField('Wednesday Open', validators=[
        Optional()], choices=time_slots)
    wednesday_close = SelectField('Wednesday Close', validators=[
        Optional()], choices=time_slots)
    thursday_open = SelectField('Thursday Open', validators=[
        Optional()], choices=time_slots)
    thursday_close = SelectField('Thursday Close', validators=[
        Optional()], choices=time_slots)
    friday_open = SelectField('Friday Open', validators=[
        Optional()], choices=time_slots)
    friday_close = SelectField('Friday Close', validators=[
        Optional()], choices=time_slots)
    saturday_open = SelectField('Saturday Open', validators=[
        Optional()], choices=time_slots)
    saturday_close = SelectField('Saturday Close', validators=[
        Optional()], choices=time_slots)
    sunday_open = SelectField('Sunday Open', validators=[
        Optional()], choices=time_slots)
    sunday_close = SelectField('Sunday Close', validators=[
        Optional()], choices=time_slots)
