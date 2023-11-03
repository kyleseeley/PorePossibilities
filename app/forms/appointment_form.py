from flask_wtf import FlaskForm
from wtforms import TextAreaField, TimeField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, Length, NumberRange


def service_data(form, field):
    serviceId = field.data
    if not serviceId:
        raise ValidationError(
            "Please select the service(s) you would like")
    
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
    serviceId = SelectField('Service', validators=[DataRequired()])
    employeeId = SelectField('Employee', validators=[DataRequired()])
    appointmentDate = DateField('Date', validators=[DataRequired()])
    appointmentTime = TimeField('Time', validators=[DataRequired()])
