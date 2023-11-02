from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError, Length, URL


def name_data(form, field):
    name = field.data
    if not name:
        raise ValidationError(
            "Please enter in a name")


def url_data(form, field):
    url = field.data
    if not url:
        raise ValidationError(
            "Please enter in a url")


def validate_image_url(form, field):
    if field.data:
        if not URL().regex.match(field.data):
            raise ValidationError("Invalid URL format for the image.")


class ImageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_data])
    imageUrl = StringField(
        'URL', validators=[DataRequired(), url_data, validate_image_url])
