# import the function that will return an instance of a connection
from recipies_app.config.mysqlconnection import connectToMySQL
from recipies_app.models import recipe_model
from flask import flash
from recipies_app import DATABASE, app, BCRYPT
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)    # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

# model the class after the friend table from our database
class User:
    db = 'recipies_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
    # Now we use class methods to query our database

    @classmethod
    def users_with_recipies( cls , id):
        data = {"id":id}
        query = "SELECT * FROM users LEFT JOIN recipies ON recipies.users_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        user = cls( results[0] )
        recipes = []
        for row_from_db in results:
            # Now we parse the ninja data to make instances of ninjas and add them into our list.
            recipe_data = {  
                "id" : row_from_db["recipies.id"],
                "name" : row_from_db["name"],
                "discription" : row_from_db["discription"],
                "instructions" : row_from_db["instructions"],
                "under" : row_from_db["under"],
                "created_at" : row_from_db["recipies.created_at"],
                "updated_at" : row_from_db["recipies.updated_at"],
                "user_id" : row_from_db["user_id"]
            }
            recipes.append( recipe_model.Recipe( recipe_data ) )
        user.recipes = recipes
        return user

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def get_id(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM users_valid
            WHERE id = %(id)s;
        """
        return cls(connectToMySQL(cls.DB).query_db( query, data )[0])
    
    @classmethod
    def get_one(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )
        results = connectToMySQL(cls.db).query_db( query, data )
        user = cls(results[0])
        return user
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE users
        SET
        first_name = %(first_name)s,
        last_name = %(last_name)s,
        email = %(email)s
        WHERE id = %(id)s;
        """
        connectToMySQL('users_schema').query_db( query, data )

    @classmethod
    def delete(cls,id):
        data = {
            "id" : id
        }
        query = """
        DELETE FROM users
        WHERE id=%(id)s;
        """
        connectToMySQL('users_schema').query_db( query, data )

    
    @classmethod
    def validate(cls, form):
        is_valid = True # we assume this is true
        if len(form['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('invalid email')
            is_valid = False
        elif cls.get_by_email(form['email']):
            flash('email already registered')
        if form['password'] != form['confirm_password']:
            flash('passwords do not match')
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, form):

        hash = BCRYPT.generate_password_hash( form['password'])
        print(hash)
        query = """INSERT INTO users ( first_name , last_name , email , password ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s);"""
        # data is a dictionary that will be passed into the save method from server.py
        form = {
            **form,
            "password" : hash
        }
        return connectToMySQL(cls.db).query_db( query, form )
    
    @classmethod
    def get_by_email(cls, email):
        data = {
            'email' : email
        }

        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        """
        results = connectToMySQL(cls.db).query_db( query, data)
    
        if results:
            return cls(results[0])

        else:
            return False

    @classmethod
    def login(cls, form):
        valid_email = cls.get_by_email(form['email'])
        if valid_email:
            if BCRYPT.check_password_hash( valid_email.password, form['password']):
                return valid_email
            else:
                flash('Invalid password')
                return False
        else:
            flash("Invalid email!")
            return False
