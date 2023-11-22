from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


def type_data(form, field):
    type = field.data
    if not type:
        raise ValidationError(
            "Please select type for the service")


def name_data(form, field):
    name = field.data
    if not name:
        raise ValidationError(
            "Please enter in a name for the service")


def price_data(form, field):
    price = field.data
    if not price:
        raise ValidationError(
            "Please enter in a price for the service")
    if price < 0:
        raise ValidationError("Price must be a positive number")


def description_data(form, field):
    description = field.data
    if not description:
        raise ValidationError(
            "Please enter in a description for the service")
    
def duration_data(form, field):
    duration = field.data
    if not duration:
        raise ValidationError(
            "Please enter in a duration for the service")
    
def image_data(form, field):
    data = field.data
    if not data:
        raise ValidationError(
            "Please enter in an image file or a URL")
    
def validate_image(form, field):
    data = field.data
    if data:
        if data.startswith("http://") or data.startswith("https://"):
            return
        filename = data
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            raise ValidationError("Invalid image file extension.")


class ServiceForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired(), type_data], choices=[
        'Skincare Treatments', 'Advanced Skincare Treatments', 'Signature Skin Therapies', 'Injectable Treatments'
    ])
    name = StringField('Name', validators=[DataRequired(), name_data])
    price = IntegerField('Price', validators=[DataRequired(), price_data])
    description = TextAreaField('Description', validators=[
        DataRequired(), description_data])
    duration = IntegerField('Duration', validators=[DataRequired(), duration_data])
    imageId = SelectField('Select Image', coerce=int)
