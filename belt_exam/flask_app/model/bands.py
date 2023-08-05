from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.model import reg_login
from flask import flash

class Band:
    def __init__(self,data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        
    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO bands
                (band_name,genre,city,user_id)
                VALUES (%(band_name)s,%(genre)s,%(city)s,%(user_id)s);
                """
        results = connectToMySQL('band_together').query_db(query,data)
        print(results)
        
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM bands
                JOIN users on bands.user_id = users.id;
                """
        results = connectToMySQL('band_together').query_db(query)
        bands = []
        for row in results:
            this_band = cls(row)
            data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': '',
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_band.creator = reg_login.User(data)
            bands.append(this_band)
        return bands
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM bands
                JOIN users on bands.user_id = users.id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL('band_together').query_db(query,data)
        if not results:
            return False
        results = results[0]
        this_band = cls(results)
        data = {
            'id': results['users.id'],
            'first_name': results['first_name'],
            'last_name': results['last_name'],
            'email': results['email'],
            'password': results['password'],
            'created_at': results['created_at'],
            'updated_at': results['updated_at']
        }
        this_band.creator = reg_login.User(data)
        return this_band
    
    @classmethod
    def get_user(cls,data):
        query = """
                SELECT * FROM users
                JOIN bands on bands.user_id = users.id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL('band_together').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        results = connectToMySQL('band_together').query_db(query,data)
        return cls(results[0])
    

    @classmethod
    def update(cls,data):
        query = """
                UPDATE bands
                SET band_name = %(band_name)s,
                genre = %(genre)s,
                city = %(city)s
                WHERE id = %(id)s;
                """
        return connectToMySQL('band_together').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        return connectToMySQL('band_together').query_db(query,data)
    
    @staticmethod
    def validate_band(band):
        is_valid = True
        if len(band['band_name']) < 2:
            flash("Name must be at least 2 characters.","createError")
            is_valid = False
        if len(band['genre']) < 2:
            flash("Genre must be at least 2 characters.","createError")
            is_valid = False
        if len(band['city']) < 3:
            flash("City must be at least 3 characters.","createError")
            is_valid = False
        return is_valid