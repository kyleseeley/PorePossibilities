from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length


def blogpost_data(form, field):
    blog = field.data
    if not blog:
        raise ValidationError(
            "Please enter in data with a minimum of 10 characters")


class BlogPostForm(FlaskForm):
    blog = TextAreaField('Blog', validators=[
        DataRequired(), blogpost_data, Length(min=10)])
