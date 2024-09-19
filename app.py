"""Taskify Hub application routes"""

# Import necessary modules
from app_factory import app, db, mail
from database import Reg, Todo
from datetime import datetime, date
from flask import flash, render_template, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Message
from model import RegisterForm, LoginForm, ResetRequestForm, ResetPasswordForm
from urllib.parse import quote

# Initialize Bootstrap
Bootstrap(app)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Create tables within application context
with app.app_context():
    # db.drop_all()
    db.create_all()

# Initialize Flask-Login for user authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Function to load a user
@login_manager.user_loader
def load_user(reg_idd):
    return Reg.query.get(str(reg_idd))

# Homepage route
@app.route('/')
def home():
    return render_template('dashboard/home.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Reg(last_name=form.last_name.data, first_name=form.first_name.data,
                       email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for('login'))
    return render_template('dashboard/reg.html', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    reset_successful = request.args.get('reset_successful', False)
    form = LoginForm()
    if form.validate_on_submit():
        user = Reg.query.filter_by(email=form.email.data).first()
        if user:
            # if not re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
            #     form.email.errors.append("Invalid email address.")
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('list'))
            else:
                form.password.errors.append('Email or Password not found.')
                # form.errors.append('Email or Password not found.')
        else:
            form.email.errors.append('Email or Password not found.')
            # form.errors.append('Email or Password not found.')
    return render_template('dashboard/login.html', form=form, reset_successful=reset_successful)

# Function to send reset password email
def send_mail(user):
    token = user.get_token()
    reset_url = url_for('reset_token', token=quote(token), _external=True)
    sender_email = 'noreply@taskifyhub.com'
    msg = Message('Taskify Hub Password Reset', recipients=[user.email], sender=sender_email)

    # HTML message with button
    html_body = render_template('dashboard/email.html', reset_url=reset_url)
    
    msg.html = html_body
    # msg.body = f''' To reset your password, please follow the link below. The link expires in 5 minutes.

    # {reset_url}

    # If you did not send a password request, please ignore this message.

    # '''
    mail.send(msg)

# Reset password request route
@app.route('/reset_request', methods=['GET', 'POST'])
def reset_password():
    form = ResetRequestForm()
    reset_successful = False
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Reg.query.filter_by(email=form.email.data).first()
            if user:
                send_mail(user)
                flash('A password reset link has been sent to your email.', 'success')
                reset_successful = True
                return redirect(url_for('login', reset_successful=reset_successful))
    return render_template('dashboard/reset_request.html', title='Reset Password',
                           form=form, reset_successful=reset_successful)

# Reset password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = Reg.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token. Please try again', 'warning')
        return redirect(url_for('reset_password'))

    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed. Please login with the new password.', 'success')
        return redirect(url_for('login'))
    return render_template('dashboard/change_password.html', form=form, token=token)

# Logout route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Add task route
@app.route('/add', methods=['POST'])
@login_required
def add():
    if (len(request.form.get('title1')) != 0):
        title = request.form.get('title1')
    else:
        title = None
        flash('Title cannot be empty.', 'title')
        return redirect(url_for('list'))
    # title = request.form.get('title1')
    description = request.form.get('description1')
    due_date_string = request.form.get('due_date')
    # Convert the string date to a Python date object
    if due_date_string:
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()
        # Check if the due date is in the past
        if due_date < date.today():
            flash('Due date has passed.', 'due_date')
            return redirect(url_for('list'))
    else:
        due_date = None
    new_todo = Todo(reg_id=current_user.idd, title=title,
                    description=description, due_date=due_date, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('list'))

# Edit task route
@app.route('/edit/<int:id>', methods=['PUT', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST':  # Check if it's a POST request
        # Check if the _method field is present and has the value 'PUT'
        if request.form.get('_method') == 'PUT':
            # Override the request method to PUT
            request.environ['REQUEST_METHOD'] = 'PUT'
    edit_todo = Todo.query.filter_by(id=id).first()
    if  edit_todo:
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_string = request.form.get('due_date')
        
        # due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()

        # Debugging output
        # print(f"Received due_date_string: {due_date_string}")
        
        if due_date_string:
            try:
                due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()
            except ValueError as e:
                print(f"Error parsing due_date_string: {e}")
                # Handling the error, e.g., by returning an error message or default value
                due_date = None
        else:
            due_date = None

        # Update the todo item
        edit_todo.title = title
        edit_todo.description = description
        edit_todo.due_date = due_date

        db.session.add(edit_todo)
        db.session.commit()
    return redirect(url_for('list'))

# Delete task route
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()

        # # Update the IDs of the remaining todos
        # remaining_todos = Todo.query.order_by(Todo.order.desc()).all()       
        # for index, todo in enumerate(remaining_todos, start=1):
        #     todo.order = index       
        # db.session.commit()
    return redirect(url_for('list'))

# Update task route
@app.route('/update/<int:id>')
@login_required
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('list'))

# Task list route
@app.route('/list', methods=['GET', 'POST'])
@login_required
def list():
    if current_user.is_authenticated:
        todo_list = Todo.query.filter_by(reg_id=current_user.idd).order_by(Todo.created_at.desc()).all()
        total_todo = Todo.query.filter_by(reg_id=current_user.idd).count()
        completed_todo = Todo.query.filter_by(reg_id=current_user.idd).filter_by(complete=True).count()
        uncompleted_todo = Todo.query.filter_by(reg_id=current_user.idd).filter_by(complete=False).count()

        # Renumbering the tasks in ascending order
        for index, todo in enumerate(todo_list):
            todo.order = index + 1
        db.session.commit()

        page = request.args.get('page', 1, type=int)
        per_page = 5
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (total_todo + per_page - 1) // per_page
        task_on_page = todo_list[start:end]

        return render_template('dashboard/list.html', **locals())
    else:
        # Handle the case when the user is not authenticated
        # For example, you can redirect them to the login page or display a message
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

# About route
@app.route('/about')
def about():
    return render_template('dashboard/about.html')

# Contact route
@app.route('/contact')
def contact():
    return render_template('dashboard/contact.html')


# Run the Flask app
if __name__ == "__main__":
    """ Main Function """
    app.run(host="127.0.0.1", port=5000, debug=True)
