"""Database creation"""
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

# Create Registration/User Models for sqlite database
class Reg(db.Model, UserMixin):
    idd = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    # overriding the default implementation provided by UserMixin and ensuring
    # that Flask-Login can retrieve the user's unique identifier correctly.
    def get_id(self):
        return self.idd

# Create List Tasks Models for sqlite database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #, autoincrement=True)
    reg_id = db.Column(db.String, db.ForeignKey('reg.idd'), nullable=False)
    order = db.Column(db.Integer, nullable=False)  # New column for task order
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    complete = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)  # New column for due date

    def __init__(self, reg_id, title, description, complete, due_date=None):
        self.reg_id = reg_id
        self.title = title
        self.description = description
        self.complete = complete
        self.due_date = due_date  # Initialize due date
        # Automatically set the order based on the current number of tasks for the user
        self.order = Todo.query.filter_by(reg_id=reg_id).count() + 1

