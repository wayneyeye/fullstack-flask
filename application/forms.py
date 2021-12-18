from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Login")
class RegisterForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    first_name = StringField("First Name",validators=[DataRequired()])
    last_name = StringField("Last Name",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    password_confirm = PasswordField("Password Confirm",validators=[DataRequired()])
    submit=SubmitField("Register")