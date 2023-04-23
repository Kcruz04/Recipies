# recipies.py
from recipies_app import app
from flask import render_template,redirect,request,session,flash
from recipies_app.models.recipe_model import Recipe
from recipies_app.models.user_model import User

@app.route("/recipes")
def recipes():
    if not 'uid' in session:
        return redirect('/')
    # call the get all classmethod to get all recipies
    recipes = Recipe.recipes_with_users()
    user = User.get_one(session['uid'])
    print(recipes)
    # return results
    return render_template("recipes.html", recipes=recipes, user = user)

# relevant code snippet from server.py
#This takes the anchor tag to create a new user and returns creat.html

@app.route('/new_recipe')
def new_recipe():
    if not 'uid' in session:
        return redirect('/')
    return render_template("new_recipe.html")

@app.route('/create_recipe', methods=["POST"])
def create_recipe():
    if not 'uid' in session:
        return redirect('/')
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "name" : request.form["name"],
        "discription" : request.form["discription"],
        "instructions" : request.form["instructions"],
        "under" : request.form["under"],
        "user_id" : request.form["user_id"]
    }
    print(request.form)
    # We pass the data dictionary into the save method from the User class.
    Recipe.save(data)
    #If values in html are same as in db we can use
    #@app.route('/friends/create', methods=['POST'])
    # def create_friend():
    #     Friend.save(request.form)
    #     return redirect('/')
    # Don't forget to redirect after saving to the database.
    return redirect('/recipes')
    
@app.route('/dashboard')
def dashboard():

    return render_template("recipes.html")

#Recieves requests from client direct to  show, edit, or delete and pages
@app.route('/show_recipe/<int:id>')
def one_recipe(id):
    recipe = Recipe.get_one(id)
    return render_template("show_recipe.html", recipe = recipe)

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if not 'uid' in session:
        return redirect('/')
    recipe = Recipe.get_one(id)
    return render_template("edit_recipe.html", recipe = Recipe.get_one(id))

@app.route('/update_recipe', methods = ["POST"])
def update_recipe():
    if not 'uid' in session:
        return redirect('/')
    print(request.form)
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    print(id)
    Recipe.delete(id)
    return redirect('/recipes')
