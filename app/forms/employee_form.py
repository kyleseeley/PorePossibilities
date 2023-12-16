from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Optional
from app.models import Employee
import re


def employee_exists(form, field):
    # Checking if user exists
    email = field.data
    if current_user.is_authenticated and current_user.email == email:
        employee = Employee.query.filter(Employee.email == email).all()
        if len(employee) > 1:
            raise ValidationError('Email address is already in use.')
    else:
        employee = Employee.query.filter(Employee.email == email).first()
        if employee:
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


def validate_email(form, field):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", field.data):
        raise ValidationError("Invalid email address")


class EmployeeForm(FlaskForm):
    time_slots = [
        '9:00 AM', '9:15 AM', '9:30 AM', '9:45 AM', '10:00 AM',
        '10:15 AM', '10:30 AM', '10:45 AM', '11:00 AM', '11:15 AM',
        '11:30 AM', '11:45 AM', '12:00 PM', '12:15 PM', '12:30 PM',
        '12:45 PM', '1:00 PM', '1:15 PM', '1:30 PM', '1:45 PM',
        '2:00 PM', '2:15 PM', '2:30 PM', '2:45 PM', '3:00 PM',
        '3:15 PM', '3:30 PM', '3:45 PM', '4:00 PM', '4:15 PM',
        '4:30 PM', '4:45 PM', '5:00 PM', '5:15 PM', '5:30 PM',
        '5:45 PM', '6:00 PM', 'Off'
    ]

    firstname = StringField('First Name', validators=[
                            DataRequired(), firstname_data, Length(min=2)])
    lastname = StringField('Last Name', validators=[
                           DataRequired(), lastname_data, Length(min=2)])
    email = StringField('Email', validators=[
                        DataRequired(), validate_email, employee_exists])
    password = PasswordField('Password', validators=[DataRequired()])
    authorized = BooleanField('Authorized', validators=[
        Optional()])
    about = TextAreaField('About', validators=[
        Optional()])
    job_tite = StringField('Job Title', validators=[
        Optional()])
    monday_start = SelectField('Monday Start', validators=[
        Optional()], choices=time_slots)
    monday_end = SelectField('Monday End', validators=[
        Optional()], choices=time_slots)
    tuesday_start = SelectField('Tuesday Start', validators=[
        Optional()], choices=time_slots)
    tuesday_end = SelectField('Tuesday End', validators=[
        Optional()], choices=time_slots)
    wednesday_start = SelectField('Wednesday Start', validators=[
        Optional()], choices=time_slots)
    wednesday_end = SelectField('Wednesday End', validators=[
        Optional()], choices=time_slots)
    thursday_start = SelectField('Thursday Start', validators=[
        Optional()], choices=time_slots)
    thursday_end = SelectField('Thursday End', validators=[
        Optional()], choices=time_slots)
    friday_start = SelectField('Friday Start', validators=[
        Optional()], choices=time_slots)
    friday_end = SelectField('Friday End', validators=[
        Optional()], choices=time_slots)
    saturday_start = SelectField('Saturday Start', validators=[
        Optional()], choices=time_slots)
    saturday_end = SelectField('Saturday End', validators=[
        Optional()], choices=time_slots)
    sunday_start = SelectField('Sunday Start', validators=[
        Optional()], choices=time_slots)
    sunday_end = SelectField('Sunday End', validators=[
        Optional()], choices=time_slots)

    def validate_start_end_times(self):
        for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            start_time_field = getattr(self, f"{day}_start")
            end_time_field = getattr(self, f"{day}_end")

            if start_time_field.data == 'Off' and end_time_field.data == 'Off':
                start_time_field.data = None
                end_time_field.data = None
            elif start_time_field.data == 'Off' or end_time_field.data == 'Off':
                self.errors[f"{day}_start"] = [
                    "Both start and end times must be 'Off'"]

    def validate(self):
        if not super().validate():
            return False

        self.validate_start_end_times()

        return True
