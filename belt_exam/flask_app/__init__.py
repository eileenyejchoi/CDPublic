from flask import Flask
app = Flask(__name__)
app.secret_key = "don't forget the key!"

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)