"""Database creation"""

# Import necessary modules
from app_factory import app, db
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from itsdangerous import TimedSerializer
from urllib.parse import unquote
from uuid import uuid4

# Create Registration/User Models for sqlite database
class Reg(db.Model, UserMixin):
    idd = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    # Override the default implementation of get_id to return the user's unique identifier
    def get_id(self):
        return self.idd
    
    # Generate a token for user authentication with an expiration time
    def get_token(self, expires_sec=300):
        serial = TimedSerializer(app.config['SECRET_KEY'])
        expiration_time = datetime.utcnow() + timedelta(seconds=expires_sec)
        return serial.dumps({'user_id': self.idd, 'exp': expiration_time.timestamp()})
        # return serial.dumps({'user_id': self.idd}, expires_in=expires_sec).decode('utf-8')

    # Verify the token to authenticate the user
    @staticmethod
    def verify_token(token):
        serial = TimedSerializer(app.config['SECRET_KEY'])
        try:
            data = serial.loads(unquote(token))
            user_id = data['user_id']
        except:
            return None
        return Reg.query.get(user_id)

# Create List Tasks Models for sqlite database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_id = db.Column(db.String, db.ForeignKey('reg.idd'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    complete = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order = db.Column(db.Integer, nullable=False)

    # Initialize List Tasks object with provided parameters
    def __init__(self, reg_id, title, description, complete, due_date=None):
        self.reg_id = reg_id
        self.title = title
        self.description = description
        self.complete = complete
        self.due_date = due_date
        self.order = Todo.query.filter_by(reg_id=reg_id).order_by(Todo.created_at.desc()).count() + 1
