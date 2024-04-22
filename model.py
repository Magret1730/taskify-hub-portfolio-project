"""Models"""
from collections.abc import Sequence
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired
from database import Reg, Todo, db
import re

class RegisterForm(FlaskForm):
    last_name = StringField(validators=[InputRequired(), Length(
        min=3, max=30)], render_kw={"placeholder": "Last Name"})
    first_name = StringField(validators=[InputRequired(), Length(
        min=3, max=30)], render_kw={"placeholder": "First Name"})
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_email(self, email):
        # Check if the email is  existing
        existing_user_email = Reg.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("Email already exist.")
        # Check if email is valid using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError("Invalid email address.")
    
    # validate last_name
    def validate_last_name(self, last_name):
        if not last_name.data.isalpha():
            raise ValidationError("Last name must contain only alphabets.")

    # validate first_name
    def validate_first_name(self, first_name):
        if not first_name.data.isalpha():
            raise ValidationError("First name must contain only alphabets.")
        
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

# class ResetPasswordRequestForm(FlaskForm):
#     email = StringField("Email", validators=[DataRequired(), Email()])
#     submit = SubmitField("Request Password Reset")
