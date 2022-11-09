from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.assignment import Assignment
from flask_app import app


@app.route("/AddAssignment")
def AddAssignment():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    return render_template("new_form.html")


@app.route('/CreateAssignment', methods=["POST"])
def CreateAssignment():
    if len(request.form['class_name']) < 1:
        flash('Class must be greater than 0')
        is_valid = False
        return redirect('/AddAssignment')

    if len(request.form['assignment_name']) < 3:
        flash('The assignment must be a minimum of 3 characters')
        is_valid = False
        return redirect('/AddAssignment')

    if len(request.form['date_due']) < 0:
        flash('The date due must be proper format 00/00/0000')
        is_valid = False
        return redirect('/AddAssignment')

    if len(request.form['notes']) < 3:
        flash('Notes should be greater than 3')
        is_valid = False
        return redirect('/AddAssignment')


    data = {
        "class_name": request.form["class_name"],
        "assignment_name" : request.form["assignment_name"],
        "date_due" : request.form["date_due"],
        "notes" : request.form["notes"],
        "user_id" : session["user_id"]
    }
    assignment_due_id = Assignment.save(data)
    session['assignment_due_id'] = assignment_due_id
    return redirect('/dashboard')

@app.route('/ShowAssignment/<int:assignment_due_id>/show')
def ShowAssignment(assignment_due_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": assignment_due_id
    }
    return render_template("assignment_detail.html", one_assignment=Assignment.get_one_assignment_with_creator(data))

@app.route('/EditAssignment/<int:assignment_due_id>/edit')
def EditAssignment(assignment_due_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        "id": assignment_due_id
    }
    return render_template("edit_assignment.html", one_assignment=Assignment.get_one(data))

@app.route('/UpdateAssignment/<int:assignment_due_id>/update', methods=["POST"])
def UpdateAssignment(assignment_due_id):

    if len(request.form['class_name']) < 1:
        flash('Class must be greater than 0')
        is_valid = False
        return redirect('/EditAssignment/<int:assignment_due_id>/edit')

    if len(request.form['assignment_name']) < 3:
        flash('The assignment must be a minimum of 3 characters')
        is_valid = False
        return redirect('/EditAssignment/<int:assignment_due_id>/edit')

    if len(request.form['date_due']) < 0:
        flash('The date due must be proper format 00/00/0000')
        is_valid = False
        return redirect('/EditAssignment/<int:assignment_due_id>/edit')

    if len(request.form['notes']) < 3:
        flash('Notes should be greater than 3')
        is_valid = False
        return redirect('/EditAssignment/<int:assignment_due_id>/edit')

    data = {
        "id": assignment_due_id,
        "class_name": request.form["class_name"],
        "assignment_name" : request.form["assignment_name"],
        "date_due" : request.form["date_due"],
        "notes" : request.form["notes"],
        "creator" : session["user_id"]
    }
    Assignment.update(data)
    return redirect('/dashboard')

@app.route('/DeleteAssignment/<int:assignment_id>/delete')
def DeleteAssignment(assignment_id):
    data = {
        "id": assignment_id
    }
    Assignment.delete(data)
    return redirect("/dashboard")

@app.route('/CompleteAssignment/<int:assignment_due_id>/complete')
def CompleteAssignment(assignment_due_id):
    data = {
        "id": assignment_due_id
    }
    Assignment.delete(data)
    return redirect("/dashboard")



