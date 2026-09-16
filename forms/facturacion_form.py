from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturaForm(FlaskForm):

    cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[DataRequired()]
    )

    total = DecimalField(
        "Total",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    submit = SubmitField("Registrar Factura")