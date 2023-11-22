from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError, Length, URL


def name_data(form, field):
    name = field.data
    if not name:
        raise ValidationError(
            "Please enter in a name")


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


class ImageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_data])
    imageFile = StringField(
        'Image File or URL', validators=[DataRequired(), image_data, validate_image])
