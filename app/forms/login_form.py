from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError, Email
from app.models import User, Employee


def user_or_employee_exists(form, field):
    # Checking if user or employee exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    employee = Employee.query.filter(Employee.email == email).first()

    if not user and not employee:
        raise ValidationError('Email provided not found.')


def password_matches(form, field):
    # Checking if password matches
    password = field.data
    email = form.data['email']

    user = User.query.filter(User.email == email).first()
    employee = Employee.query.filter(Employee.email == email).first()

    if user and not user.check_password(password):
        raise ValidationError('Password was incorrect.')
    if employee and not employee.check_password(password):
        raise ValidationError('Password was incorrect.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), user_or_employee_exists])
    password = StringField('Password', validators=[
                           DataRequired(), password_matches])
