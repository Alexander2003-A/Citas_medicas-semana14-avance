from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField
)

from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )

    proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Registrar Producto")