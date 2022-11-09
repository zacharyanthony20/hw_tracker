from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user


class Assignment:
    def __init__( self , data ):
        self.id = data['id']
        self.class_name = data['class_name']
        self.assignment_name = data['assignment_name']
        self.date_due = data['date_due']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM assignment_due where id=%(id)s;"

        results = connectToMySQL('homework_tracker').query_db(query)

        assignment_due = []

        for assignment_due in results:
            assignment_due.append( cls(assignment_due) )
        return assignment_due

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM assignment_due where id=%(id)s;"
        results = connectToMySQL('homework_tracker').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO assignment_due (class_name, assignment_name, date_due, notes, created_at, updated_at, user_id) VALUES (%(class_name)s, %(assignment_name)s, %(date_due)s, %(notes)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def update(cls, data):
        query = "UPDATE assignment_due SET class_name=%(class_name)s, assignment_name=%(assignment_name)s, date_due=%(date_due)s, notes=%(notes)s WHERE id=%(id)s;"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM assignment_due WHERE id=%(id)s"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def get_all_assignment_with_creator(cls):

        query = "SELECT * FROM assignment_due JOIN user ON assignment_due.user_id = user.id;"
        results = connectToMySQL('homework_tracker').query_db(query)
        all_assignment = []
        for row in results:

            one_assignment = cls(row)

            one_assignment_author_info = {
                "id": row['user.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['user.created_at'],
                "updated_at": row['user.updated_at']
            }

            author = user.User(one_assignment_author_info)

            one_assignment.creator = author

            all_assignment.append(one_assignment)
        return all_assignment

    @classmethod
    def get_one_assignment_with_creator(cls, data):
        query = "SELECT * FROM assignment_due JOIN user ON assignment_due.user_id = user.id WHERE assignment_due.id=%(id)s;"
        results = connectToMySQL('homework_tracker').query_db(query, data)
        if len(results) < 1:
            return False

        for row in results:
            one_assignment = cls(row)
            one_assignment_author_info = {
                "id": row['user.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['user.created_at'],
                "updated_at": row['user.updated_at']
            }

            author = user.User(one_assignment_author_info)
            one_assignment.creator = author
        return one_assignment

@staticmethod
def validate_assignment(assignment_dict):
    valid = True
    flash_string = "All fields required"
    if len(assignment_dict["price"]) < 0:
        flash("price" + "must be greater than 0")
        valid = False
    if len(assignment_dict["model"]) < 0:
        flash("price" + "cannot be left blank")
        valid = False
    if len(assignment_dict["make"]) < 0:
        flash("make" + "cannot be left blank")
        valid = False
    if len(assignment_dict["year"]) < 0:
        flash("year" + "must be greater than 0")
        valid = False
    if len(assignment_dict["description"]) < 3:
        flash("description" + "must be greater than 3")
        valid = False

    return valid