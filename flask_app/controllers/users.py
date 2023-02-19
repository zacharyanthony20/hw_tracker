from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.assignment import Assignment


from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

def is_user_logged_in():
    return 'user_id' in session

def is_user_authenticated():
    if not is_user_logged_in():
        return False
    user_id = session['user_id']
    return User.get_one({'id': user_id}) is not None

def requires_authentication(route_function):
    def wrapper_function(*args, **kwargs):
        if not is_user_authenticated():
            flash('You must be logged in to view this page')
            return redirect('/')
        return route_function(*args, **kwargs)
    return wrapper_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def validate_register():
    print("validate_register function called")
    flash_messages = []
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password']
    }
    if len(request.form['first_name']) < 3:
        flash_messages.append('The first name must be a minimum of 3 characters')
    if len(request.form['last_name']) < 3:
        flash_messages.append('The last name must be a minimum of 3 characters')
    if not User.validateEmail(request.form):
        flash_messages.append('The email address was not valid')
    if User.get_one_email(request.form):
        flash_messages.append('The email address already exists')
    if len(request.form['password']) < 8:
        flash_messages.append('The password must be at least 8 characters long')
    if request.form['password'] != request.form['confirm']:
        flash_messages.append('The password and confirm password did not match')

    for message in flash_messages:
        flash(message, category='registration')

    if len(flash_messages) > 0:
        flash(' '.join(flash_messages))
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = pw_hash
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['route'] = 'register'
    return redirect('/dashboard')

@app.route('/dashboard')
@requires_authentication
def show_user():
    user_id = session['user_id']
    data = {
        "id": user_id
    }
    return render_template("dashboard.html", one_user=User.get_one(data), all_assignment=Assignment.get_all_assignment_with_creator())

@app.route('/login', methods=['POST'])
def validate_login():
    flash_messages = []
    email = request.form['email']
    password = request.form['password']

    if not email:
        flash_messages.append('Please enter your email')
    if not password:
        flash_messages.append('Please enter your password')
    if email and not User.get_one_email(request.form):
        flash_messages.append('The email address is not registered')
    if email and password and User.get_one_email(request.form):
        user = User.get_one_email(request.form)
        if not bcrypt.check_password_hash(user.password, password):
            flash_messages.append('The password is incorrect')
    
    if flash_messages:
        for message in flash_messages:
            flash(message, category='login')
        return redirect('/')
    
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['route'] = 'login'
    return redirect('/dashboard')
