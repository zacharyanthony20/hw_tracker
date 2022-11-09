from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.assignment = []


    @staticmethod
    def validateEmail(user):
        isValid = True
        if not EMAIL_REGEX.match(user['email']): 
            isValid = False
        return isValid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"

        results = connectToMySQL('homework_tracker').query_db(query)

        user = []

        for user in results:
            user.append( cls(user) )
        return user

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM user where id=%(id)s;"
        results = connectToMySQL('homework_tracker').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def update(cls, data):
        query = "UPDATE user SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, WHERE id=%(id)s;"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM user WHERE id=%(id)s"
        return connectToMySQL('homework_tracker').query_db( query, data )   

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM user where email=%(email)s;"
        results = connectToMySQL('homework_tracker').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one_assignment(cls, data):
        query = "SELECT * FROM user JOIN assignment where user.id=%(id)s;"
        results = connectToMySQL('homework_tracker').query_db(query, data)
        user = []

        for user in results:
            user.append( cls(user) )
        return user
