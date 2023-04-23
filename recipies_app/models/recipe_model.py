# import the function that will return an instance of a connection
from recipies_app.config.mysqlconnection import connectToMySQL
from recipies_app.models import user_model
# model the class after the friend table from our database
class Recipe:
    db = 'recipies_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.discription = data['discription']
        self.instructions = data['instructions']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    # Now we use class methods to query our database

    @classmethod
    def recipes_with_users( cls ):
        query = "SELECT * FROM recipies JOIN users ON recipies.user_id = users.id ;"
        results = connectToMySQL(cls.db).query_db( query)
        # results will be a list of topping objects with the burger attached to each row. 
        recipes = []
        if results:
            for row_from_db in results:
                
                recipe = Recipe(row_from_db)
                # Now we parse the ninja data to make instances of ninjas and add them into our list.
                user_data = {  
                    "id" : row_from_db["users.id"],
                    "first_name" : row_from_db["first_name"],
                    "last_name" : row_from_db["last_name"],
                    "password" : row_from_db["password"],
                    "email" : row_from_db["email"],
                    "created_at" : row_from_db["users.created_at"],
                    "updated_at" : row_from_db["users.updated_at"],
                }
                user = user_model.User(user_data)
                recipe.user = user
                recipes.append(recipe)
        return recipes

    @classmethod
    def save(cls, data):

        query = """INSERT INTO recipies ( name , discription , instructions , under, user_id ) 
        VALUES ( %(name)s , %(discription)s , %(instructions)s , %(under)s , %(user_id)s ) ;"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipies;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes
    
    @classmethod
    def get_one(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM recipies
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )
        results = connectToMySQL(cls.db).query_db( query, data )
        recipe = cls(results[0])
        return recipe
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipies
        SET
        name = %(name)s,
        discription = %(discription)s,
        instructions = %(instructions)s,
        under = %(under)s
        WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def delete(cls,id):
        data = {
            "id" : id
        }
        query = """
        DELETE FROM recipies
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db( query, data )
    
