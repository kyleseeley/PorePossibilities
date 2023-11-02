from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, ValidationError, Length


def blogpost_title(form, field):
    title = field.data
    if not title:
        raise ValidationError(
            "Please enter in a title")


def blogpost_data(form, field):
    blog = field.data
    if not blog:
        raise ValidationError(
            "Please enter in data with a minimum of 10 characters")


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[
                        DataRequired(), blogpost_title, Length(min=3)])
    blog = TextAreaField('Blog', validators=[
        DataRequired(), blogpost_data, Length(min=10)])
