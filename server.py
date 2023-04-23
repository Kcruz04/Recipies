from recipies_app import app

from recipies_app.controllers import users_controller, recipies_controller
# ...server.py

if __name__ == "__main__":
    app.run(debug = True, port = 5001)