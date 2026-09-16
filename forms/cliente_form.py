from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[DataRequired()]
    )

    cedula = StringField(
        "Cédula",
        validators=[DataRequired()]
    )

    telefono = StringField(
        "Teléfono",
        validators=[DataRequired()]
    )

    correo = StringField(
        "Correo",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Registrar Cliente")