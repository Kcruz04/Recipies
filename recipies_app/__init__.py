from flask import Flask
app=Flask(__name__)

app.secret_key = "rootroot"

from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt(app)

DATABASE = "recipies_schema"

