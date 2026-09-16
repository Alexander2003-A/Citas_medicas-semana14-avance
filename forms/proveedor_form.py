from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(min=7, max=20)
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField("Registrar Proveedor")