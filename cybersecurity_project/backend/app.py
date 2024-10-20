
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import os
import secrets

app = Flask(__name__)

secureKey = secrets.token_hex(64)
jwtKey = secrets.token_hex(64)

dbPath = os.path.join(os.path.dirname(__file__), 'transactions.db')
print(dbPath)

#line 14 not done, ewan ko pa pano i link url to this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbPath
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secureKey)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', jwtKey)

dBase = SQLAlchemy(app)
bCrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(dBase.Model):
    id = dBase.Column(dBase.Integer, primary_key = True)

@app.route('/')
def home():
    return "Welcome to the Cybersecurity Dashboard!"

@app.route('/signup')
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify({"Error:" "This user already exists"}), 400
    #makes a unique password hash for each user in case of same passwords different users
    hashed_password = bCrypt.generate_pasword_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    dBase.session.add(new_user)
    dBase.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username = username).first()
    #checks if username is valid or if the password matches the one with the hash assigned to the username
    if not user or not bCrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid user or password"}), 401
    #no clue ano to rn
    accessToken = create_access_token(identity = username)
    return jsonify({"Access token": accessToken}), 200
    
@app.route('/dashboard', methods = ['GET'])
@jwt_required()

def dashboard():
    currentUser = get_jwt_identity()
    return jsonify({"Message": "something remind me to change this part" })

if __name__ == '__main__':
    app.run(debug=True)
