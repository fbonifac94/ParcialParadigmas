from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField;
from wtforms.validators import Required;

class IngresoForm(FlaskForm):
    usuario = StringField('Ingrese usuario:', validators=[Required()]);
    contrasenia = PasswordField('Ingrese contraseña:', validators=[Required()]);
    submit = SubmitField('Ingresar');

class RegistroForm(IngresoForm):
    confirmContrasenia = PasswordField('Reingrese contraseña:', validators=[Required()]);    
    submit = SubmitField('Registrarse');
    
    