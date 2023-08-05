from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model import bands
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL('band_together').query_db(query,data)
        return results
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('band_together').query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
        return users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('band_together').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('band_together').query_db(query,data)
        if not results:
            return False
        return cls(results[0])
    
    
    @staticmethod
    def validate_reg(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Invalid First Name. Must be at least 3 characters.","regError")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Invalid Last Name. Must be at least 3 characters.","regError")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('band_together').query_db(query,user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email.","regError")
            is_valid = False
        if len(user['password']) < 8:
            flash("Invalid Password. Must be at least 8 characters.","regError")
            is_valid = False
        elif user['password'] != user['confirm']:
            flash("Passwords did not match.","regError")
            is_valid = False
        this_user = User.get_by_email(user)
        print(this_user)
        if this_user:
            is_valid = False
            flash("Email unavailable.","regError")
        return is_valid
    
    