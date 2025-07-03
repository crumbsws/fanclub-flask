from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import jsonify, request, make_response
from sqlalchemy import or_
from fanclub.models.user_model import User  # Updated import path
from flask import current_app as app
from fanclub.extensions import db  # Updated import path
import uuid



def login_user(data):
    
    response = make_response()
    identifier = data.get('identifier')
    password = data.get('password')

    if not identifier or not password:
        return {"error": "Missing identifier or password"}, 400

    
    user = User.query.filter(
        or_(
            User.username == identifier,
            User.email == identifier
        )
    ).first()

    if not user:
        return {"error": "User not found"}, 404
    if not check_password_hash(user.password, password):
        return {"error": "Invalid password"}, 401

    if user and check_password_hash(user.password, password):
        token = jwt.encode({"user_id": user.id}, "secret_key", algorithm="HS256")
        response.set_cookie('jwt_token', token)

    return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat(),
                'level': user.level
            }
        }), 200

def register_user(data):
    
    response = make_response()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return {"error": "Missing username, password, or email"}, 400

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user_uuid = str(uuid.uuid4())

    new_user = User(id=user_uuid, username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({"user_id": user_uuid}, "secret_key", algorithm="HS256")
    response.set_cookie('jwt_token', token)

    return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat(),
                'level': new_user.level
            }
        }), 201

def authenticate_user(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user = User.query.filter_by(id=data['user_id']).first()
        if not user:
            return {"error": "User not found"}, 404
        return jsonify({
            'message': 'User authenticated successfully',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat(),
                'level': new_user.level
            }
        }), 201
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}, 401