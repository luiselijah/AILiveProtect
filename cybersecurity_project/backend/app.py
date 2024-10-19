from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import secrets

app = Flask(__name__)

secureKey = secrets.token_hex(64)
jwtKey = secrets.token_hex(64)

#line 14 not done, ewan ko pa pano i link url to this
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

@app.route('/signup')
def signup():
    data = request.get_json()
    username = data[username]
    password = data[password]

    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify({"Error:" "This user already exists"}), 400
    
    hashed_password = bCrypt.generate_pasword_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    dBase.session.add(new_user)
    dBase.session.commit()

    return jsonify({"message": "User created successfully"}), 201

    

if __name__ == '__main__':
    app.run(debug=True)
