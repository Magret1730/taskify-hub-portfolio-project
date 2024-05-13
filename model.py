"""Model Form"""

# Import necessary modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email, DataRequired
from database import Reg
import re

# Define Registration Form
class RegisterForm(FlaskForm):
    last_name = StringField(validators=[InputRequired(), Length(
        min=3, max=30)], render_kw={"placeholder": "Last Name"})
    first_name = StringField(validators=[InputRequired(), Length(
        min=3, max=30)], render_kw={"placeholder": "First Name"})
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register") # Define submit button label

    # Validate uniqueness of email and format of email address
    def validate_email(self, email):
        # Check if the email is  existing
        existing_user_email = Reg.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("Email already exist.")
        # Check if email is valid using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError("Invalid email address.")
    
    # validate last_name contains only alphabets
    def validate_last_name(self, last_name):
        if not last_name.data.isalpha():
            raise ValidationError("Last name must contain only alphabets.")

    # validate first_name contains only alphabets
    def validate_first_name(self, first_name):
        if not first_name.data.isalpha():
            raise ValidationError("First name must contain only alphabets.")

# Define Login Form
class LoginForm(FlaskForm):
    # Define form fields with validators and placeholders
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login") # Define submit button label

    # Validate format of email address
    def validate_email(self, email):
        # Check if the email is  existing
        existing_user_email = Reg.query.filter_by(email=email.data).first()
        if existing_user_email:
        # Check if email is valid using regular expression
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
                raise ValidationError("Invalid email address.")

# Define Reset Password Request Form
class ResetRequestForm(FlaskForm):
    # Define form fields with validators and placeholders
    email = StringField(label="Email", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Email"})
    submit = SubmitField(label="Reset Password") # Define submit button label

# Define Reset Password Form
class ResetPasswordForm(FlaskForm):
    # Define form fields with validators and placeholders
    password = PasswordField(label="Password", validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField(label="Confirm Password", validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField(label="Change Password") # Define submit button label

    # Validate if passwords match
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError("Password does not match.")
