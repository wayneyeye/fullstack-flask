from flask_wtf import FlaskForm
from werkzeug import datastructures
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
    password_confirm = PasswordField("Password Confirm",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Register Now")
    def save(self):
        table=dynamo.tables['users']
        table.put_item(Item={
            "email": self.email.data,
            "first_name": self.first_name.data,
            "last_name": self.last_name.data,
            "password": self.password,
        })
    
    # validate_<field name>
    def validate_email(self,email):
        print("Run validate email!")
        table=dynamo.tables['users']
        user=table.query(
        KeyConditionExpression=Key('email').eq(email.data)
        ).get("Items")
        if user:
            raise ValidationError("User already registered")
        else:
            return True