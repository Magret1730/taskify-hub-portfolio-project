"""Taskify Hub application routes"""
from database import Reg, Todo, db
from datetime import datetime, date
from flask import flash, Flask, render_template, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mail import Mail, Message
from model import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'dfe7b0946804edf295050cbb8ce8d3aec72063aede88df37'
Bootstrap(app)
bcrypt = Bcrypt(app)

# Initialize the database
db.init_app(app)

# Create tables within application context
with app.app_context():
    # db.drop_all()
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(reg_idd):
    return Reg.query.get(str(reg_idd))

@app.route('/')
def home():
    return render_template('dashboard/home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Reg(last_name=form.last_name.data, first_name=form.first_name.data,
                       email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('dashboard/reg.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    reset_successful = request.args.get('reset_successful', False)
    form = LoginForm()
    if form.validate_on_submit():
        user = Reg.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('list'))
            else:
                form.password.errors.append('Invalid password')
        else:
            form.email.errors.append('Email not found')
    return render_template('dashboard/login.html', form=form, reset_successful=reset_successful)

# Define the route and endpoint for password reset
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    # Add your password reset logic here
    if request.method == 'POST':
        # Process the form submission and initiate the password reset process
        # email = Reg.query.filter_by(email=request.form.email.data).first()
        email = request.form.get('email')
        if email:
            existing_user = Reg.query.filter_by(email=email).first()
            if existing_user:
                # last_name = user.last_name
                # first_name = user.first_name
                new_password = request.form.get('password')
                # new_login = Reg(email=email, last_name=last_name, first_name=first_name, password=new_password)
                hashed_password = bcrypt.generate_password_hash(new_password)
                existing_user.password = hashed_password
                # db.session.add(new_login)
                db.session.commit()
                flash('Password reset successful. Please log in with your new password.', 'success')
                # return "Password reset successful"
                return redirect(url_for('login', reset_successful=True))
            else:
                request.form.email.errors.append('Email not found')
                return redirect(url_for('reset_password'))
        else:
            request.form.email.errors.append('Email not provided')
            # flash('Email not provided', 'error')
            return redirect(url_for('reset_password'))
    return render_template('reset_password.html')
    # return redirect(url_for('list'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
@login_required
def add():
    if (len(request.form.get('title1')) != 0):
        title = request.form.get('title1')
    else:
        title = None
        flash('Title cannot be empty.', 'title')  # Flash an error message
        return redirect(url_for('list'))
    # title = request.form.get('title1')
    description = request.form.get('description1')
    due_date_string = request.form.get('due_date')
    # Convert the string date to a Python date object
    if due_date_string:
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()

        # Check if the due date is in the past
        if due_date < date.today():
            flash('Due date has already passed.', 'due_date')
            # past_due_date = date.today()  #.strftime('%Y-%m-%d')
            # # print(past_due_date)
            return redirect(url_for('list')) # past_due_date=past_due_date))
    else:
        due_date = None

    new_todo = Todo(reg_id=current_user.idd, title=title, description=description, due_date=due_date, complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for('list'))  #,past_due_date=past_due_date))

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
        
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()

        # Update the todo item
        edit_todo.title = title
        edit_todo.description = description
        edit_todo.due_date = due_date

        db.session.add(edit_todo)
        db.session.commit()
    return redirect(url_for('list'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()

        # Update the IDs of the remaining todos
        remaining_todos = Todo.query.order_by(Todo.id).all()       
        for index, todo in enumerate(remaining_todos, start=1):
            todo.id = index       
        db.session.commit()
    return redirect(url_for('list'))

@app.route('/update/<int:id>')
@login_required
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('list'))

@app.route('/list', methods=['GET', 'POST'])
# @login_required
def list():
    if current_user.is_authenticated:
        todo_list = Todo.query.filter_by(reg_id=current_user.idd).all()
        total_todo = Todo.query.filter_by(reg_id=current_user.idd).count()
        completed_todo = Todo.query.filter_by(reg_id=current_user.idd).filter_by(complete=True).count()
        uncompleted_todo = Todo.query.filter_by(reg_id=current_user.idd).filter_by(complete=False).count()
        #  OR uncompleted_todo = total_todo - completed_todo
        return render_template('dashboard/list.html', **locals())
    else:
        # Handle the case when the user is not authenticated
        # For example, you can redirect them to the login page or display a message
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('dashboard/about.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host="127.0.0.1", port=5000, debug=True)
