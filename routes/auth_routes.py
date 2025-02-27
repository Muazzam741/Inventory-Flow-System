from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import User
from db import db

auth_bp = Blueprint('auth', __name__)

# User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password required"}), 400

    # Hash password before storing
    hashed_password = generate_password_hash(data['password'])

    # Create new user
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generate JWT Token
    access_token = create_access_token(identity=user.username)
    return jsonify({"access_token": access_token}), 200
