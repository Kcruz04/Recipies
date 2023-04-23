# userss.py
from recipies_app import app
from flask import render_template,redirect,request,session,flash
from recipies_app.models.user_model import User
# from recipies_app.models.recipe_model import Recipe

@app.route('/')
def index():
    return render_template("home.html")
# relevant code snippet from server.py
#This takes the anchor tag to create a new user and returns creat.html

# @app.route('/new_user', methods=["POST"])
# def creat_user():
#     # First we make a data dictionary from our request.form coming from our template.
#     # The keys in data need to line up exactly with the variables in our query string.
#     data = {
#         "first_name": request.form["first_name"],
#         "last_name" : request.form["last_name"],
#         "email" : request.form["email"],
#         "password" : request.form["password"],
        
#     }
#     print(request.form)
#     # We pass the data dictionary into the save method from the User class.
#     User.save(data)
#     #If values in html are same as in db we can use
#     #@app.route('/friends/create', methods=['POST'])
#     # def create_friend():
#     #     Friend.save(request.form)
#     #     return redirect('/')

#     # Don't forget to redirect after saving to the database.
#     return redirect('/recipes')

@app.route('/register', methods=['POST'])
def register():
    # if not User.validate_user(request.form):
        # we redirect to the template with the form.
        print(request.form)
        # if not User.validate(request.form):
        #     return redirect('/')
        
        User.register(request.form)
        # ... do other things
        return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    valid_email = User.login(request.form)
    if valid_email:
        session['uid'] = valid_email.id
        return redirect('/recipes')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')  

@app.route("/read(all)")
def all_users():
    # call the get all classmethod to get all userss
    users = User.get_all()
    print(users)
    results= render_template("read(all).html",users=users)
    return results

#Recieves requests from client direct to  show, edit, or delete and pages
@app.route('/read(one)/<int:id>')
def one_user(id):
    users_from_controller = User.get_one(id)
    return render_template("read(one).html", users_from_controller = users_from_controller)

@app.route('/edit/<int:id>')
def edit_user(id):
    user = User.get_one(id)
    return render_template("edit.html", user = user)

@app.route('/update', methods = ["POST"])
def update_user():
    print(request.form)
    User.update(request.form)
    return redirect(f"/read(one)/{request.form['id']}")

@app.route('/delete/<int:id>')
def delete_user(id):
    print(id)
    User.delete(id)
    return redirect('/')
