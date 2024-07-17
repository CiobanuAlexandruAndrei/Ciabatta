from flask import request, jsonify
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import db
from .models import User, Profile, Token
import secrets
from . import security

auth = HTTPTokenAuth(scheme='Bearer')

@security.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return jsonify({'message': 'Missing required fields'}), 400
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    new_profile = Profile(user_id=new_user.id)
    db.session.add(new_profile)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

@security.route('/login', methods=['POST'])
def login_view():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        token = secrets.token_hex(16)
        new_token = Token(user_id=user.id, token=token)
        db.session.add(new_token)
        db.session.commit()
        return jsonify({'token': token, 'user': user.username})
    else:
        return jsonify({'error': 'Invalid credentials'}), 400

@security.route('/logout', methods=['POST'])
@auth.login_required
def logout_view():
    user = auth.current_user()
    if user:
        tokens = Token.query.filter_by(user_id=user.id).all()
        for token in tokens:
            db.session.delete(token)
        db.session.commit()
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@security.route('/username/<int:pk>', methods=['GET'])
@auth.login_required
def get_username_view(pk):
    user = auth.current_user()
    if user:
        profile = Profile.query.filter_by(user_id=user.id).first()
        if profile:
            return jsonify({'user': profile.user.username})
        else:
            return jsonify({'error': 'Profile not found'}), 404
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@auth.verify_token
def verify_token(token):
    print(f"Verifying token: {token}")  # Debug statement
    token_obj = Token.query.filter_by(token=token).first()
    if token_obj:
        print(f"Token valid for user_id: {token_obj.user_id}")  # Debug statement
        return User.query.get(token_obj.user_id)
    print("Token invalid")  # Debug statement
    return None