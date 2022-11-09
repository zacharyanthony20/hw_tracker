from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.assignment import Assignment


from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def validateRegister():
    flash_string = "All fields required"
    is_valid = True
    if len (request.form['first_name']) < 3:
        flash('The first name must be a minimum of 3 characters')
        is_valid = False
        return redirect('/')

    if len (request.form['last_name']) < 3:
        flash('The last name must be a minimum of 3 characters')
        is_valid = False
        return redirect('/')

    if not User.validateEmail(request.form):
        flash('The email address was not valid')
        is_valid = False
        return redirect('/')

    if User.get_one_email(request.form):
        flash('The email address already exists')
        is_valid = False
        return redirect('/')
    
    if len (request.form['password']) < 8:
        flash('The password must be at least 8 characters long')
        is_valid = False
        return redirect('/')

    if request.form['password'] != request.form['confirm']:
        flash('The password and confirm password did not match')
        is_valid = False
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form["email"],
        "password" : pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['route'] = 'register'
    return redirect('/dashboard')

@app.route('/dashboard')
def showUser():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')

    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html", one_user=User.get_one(data), all_assignment=Assignment.get_all_assignment_with_creator())    

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"]
    }
    user_in_db = User.get_one_email(data)
    if not user_in_db:
        flash("The Email Address is not registered")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')

    flash("Your in!!!")
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['route'] = 'login'
    return redirect('/dashboard')

@app.route('/logout')
def Logout():
    session.clear()
    return redirect('/')