from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'dfe7b0946804edf295050cbb8ce8d3aec72063aede88df37'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'belloabiodun17@gmail.com'
app.config['MAIL_PASSWORD'] = 'ekjm xvvi ofwn dwxh'

mail = Mail(app)
