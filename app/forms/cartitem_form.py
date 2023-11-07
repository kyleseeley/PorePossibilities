from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired, ValidationError


def validateQuantity(form, field):
    quantity = field.data
    if not quantity:
        raise ValidationError(
            "Please enter an amount for the item.")


class CartItemForm(FlaskForm):
    serviceId = SelectField('Service', validators=[DataRequired()])
    quantity = SelectField("Quantity", validators=[
        DataRequired(), validateQuantity,], choices=[1, 2, 3, 4, 5])
