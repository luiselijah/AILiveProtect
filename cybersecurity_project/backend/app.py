from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import secrets

app = Flask(__name__)

secureKey = secrets.token_hex(64)
jwtKey = secrets.token_hex(64)

app.config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secureKey)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', jwtKey)

dBase = SQLAlchemy(app)
bCrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(dBase.Model):
    id = dBase.Column(dBase.Integer, primary_key = True)
    username = dBase.Column(dBase.String(150), unique=True, nullable=False)
    password = dBase.Column(dBase.String(150), nullable=False)

@app.route('/')
def home():
    return "Welcome to the Cybersecurity Dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
