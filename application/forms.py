from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo,ValidationError
from application import dynamo
from flask import flash
from boto3.dynamodb.conditions import Key

# app=Flask(__name__)
class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me=BooleanField("Remember me")
    submit=SubmitField("Login")

class EnrollmentForm(FlaskForm):
    email=None # placeholder to get from session
    courseID = StringField("CourseID",validators=[DataRequired()])
    submit=SubmitField("Enroll")
    def validate_courseID(self,courseID):
        print("Run validate courseID!")
        table=dynamo.tables['enrollment']
        # email get from session
        enrollment=table.query(
        KeyConditionExpression=Key('email').eq(self.email)
        ).get("Items")
        print(list(map(lambda a:a.get("courseID"),enrollment)))
        if courseID.data in list(map(lambda a:a.get("courseID"),enrollment)):
            flash("Course already registered",category="danger")
            raise ValidationError("Course already registered")
        else:
            flash("You have successfully enrolled",category="success")
            return True

    def save(self):
        table=dynamo.tables['enrollment']
        table.put_item(Item={
            "email": self.email, # get from session
            "courseID": self.courseID.data,
        })
    
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