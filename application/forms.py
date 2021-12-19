from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo,ValidationError
from application import dynamo
from boto3.dynamodb.conditions import Key
class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Login")
class RegisterForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    first_name = StringField("First Name",validators=[DataRequired()])
    last_name = StringField("Last Name",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('Password')])
    submit=SubmitField("Register Now")
    def validate_email(self,email):
        table=dynamo.tables['users']
        user=table.query(
        KeyConditionExpression=Key('email').eq(email)
        ).get("Items",[None])[0]
        if user:
            raise ValidationError("User already registered")