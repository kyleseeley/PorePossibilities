from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, EmailField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length
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
    name = StringField('Name', validators=[
                       DataRequired(), Length(max=50), name_data])
    email = EmailField('Email', validators=[DataRequired(), validate_email])
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
