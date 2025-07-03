from flask import Blueprint, request, jsonify
from fanclub.controllers.auth import login_user, register_user, authenticate_user
from fanclub.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@auth_bp.route('/me', methods=['POST'])
@token_required
def authenticate():
    data = request.cookies.get('jwt_token')
    return authenticate_user(data)

