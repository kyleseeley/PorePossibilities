from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User
import re
import phonenumbers


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    if current_user.is_authenticated and current_user.email == email:
        user = User.query.filter(User.email == email).all()
        if len(user) > 1:
            raise ValidationError('Email address is already in use.')
    else:
        user = User.query.filter(User.email == email).first()
        if user:
            raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')


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


def validate_email(form, field):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
        raise ValidationError("Invalid email address")


def phone_data(form, field):
    phone = field.data
    try:
        parsed_phone = phonenumbers.parse(phone, "US")
        print('parsed phone', parsed_phone)
        print("valid or not", phonenumbers.is_valid_number(parsed_phone))
        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValidationError("Invalid phone number")

    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Invalid phone number format")

# def phone_data(form, field):
#     phone = field.data
#     pattern = r'^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$'

#     if not re.match(pattern, phone):
#         raise ValidationError("Invalid phone number")


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[
                            DataRequired(), firstname_data, Length(min=2)])
    lastname = StringField('Last Name', validators=[
                           DataRequired(), lastname_data, Length(min=2)])
    email = StringField('Email', validators=[
                        DataRequired(), validate_email, user_exists])
    phone = StringField('Phone', validators=[DataRequired()])
    username = StringField(
        'Username', validators=[DataRequired(), username_exists])
    address = StringField('Address', validators=[DataRequired(), address_data])
    city = StringField('City', validators=[DataRequired(), city_data])
    state = SelectField('State', validators=[DataRequired(), state_data], choices=[
        'AL - Alabama', 'AK - Alaska', 'AZ - Arizona', 'AR - Arkansas', 'CA - California', 'CO - Colorado', 'CT - Connecticut', 'DE - Delaware', 'FL - Florida', 'GA - Georgia', 'HI - Hawaii', 'ID - Idaho', 'IL - Illinois', 'IN - Indiana', 'IA - Iowa', 'KS - Kansas', 'KY - Kentucky', 'LA - Louisiana', 'ME - Maine', 'MD - Maryland',
        'MA - Massachusetts', 'MI - Michigan', 'MN - Minnesota', 'MS - Mississippi', 'MO - Missouri', 'MT - Montana', 'NE - Nebraska', 'NV - Nevada', 'NH - New Hampshire', 'NJ - New Jersey',
        'NM - New Mexico', 'NY - New York', 'NC - North Carolina', 'ND - North Dakota', 'OH - Ohio', 'OK - Oklahoma', 'OR - Oregon', 'PA - Pennsylvania', 'RI - Rhode Island', 'SC - South Carolina',
        'SD - South Dakota', 'TN - Tennessee', 'TX - Texas', 'UT - Utah', 'VT - Vermont', 'VA - Virginia', 'WA - Washington', 'WV - West Virginia', 'WI - Wisconsin', 'WY - Wyoming'
    ])
    password = PasswordField('Password', validators=[DataRequired()])
