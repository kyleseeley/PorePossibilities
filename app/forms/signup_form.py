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
    user = User.query.filter(User.username.ilike(username)).first()
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
        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValidationError("Invalid phone number")

    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Invalid phone number format")
    
def phone_data_input(form, field):
    phone = field.data
    if not phone.isdigit():
        raise ValidationError("Phone number should only contain digits.")
    
def password_data(form, field):
    password = field.data
    if len(password) < 6:
        raise ValidationError(
            "Password must be at least 6 characters")


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[
                            DataRequired(), firstname_data])
    lastname = StringField('Last Name', validators=[
                           DataRequired(), lastname_data])
    email = StringField('Email', validators=[
                        DataRequired(), validate_email, user_exists])
    phone = StringField('Phone', validators=[DataRequired(), phone_data, phone_data_input])
    username = StringField(
        'Username', validators=[DataRequired(), username_exists])
    address = StringField('Address', validators=[DataRequired(), address_data])
    city = StringField('City', validators=[DataRequired(), city_data])
    state = SelectField('State', validators=[DataRequired(), state_data], choices=[
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
        'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ])
    password = PasswordField('Password', validators=[DataRequired(), password_data])
