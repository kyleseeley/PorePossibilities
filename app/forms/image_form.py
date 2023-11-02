from flask_wtf import FlaskForm
from wtforms import URLField, StringField
from wtforms.validators import DataRequired, ValidationError, Length


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


class ImageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_data])
    imageUrl = URLField('URL', validators=[DataRequired(), url_data])
