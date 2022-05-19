#!/usr/bin/python3
"""
Define all api route functions for the user
"""


from flask_bcrypt import Bcrypt
from api.v1.views import app_views
from flask import request
import json
from flask_login import current_user

bcrypt = Bcrypt()

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Function to get all users"""
    from models import storage

    new_dict = {}
    all_users = storage.all('User')
    for k, v in all_users.items():
        key = (k.split('.', 1))[1]
        new_dict[key] = v.to_dict()
    return new_dict

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get a specific user with the provided id"""
    from models import storage

    new_dict = {}
    user = storage.get('User', user_id)
    if not user:
        return "Invalid user id"
    for k, v in user.items():
        key = (k.split('.', 1))[1]
        new_dict[key] = v.to_dict()
    return new_dict

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Function to create a new user"""
    from models import storage

    from models.users import User
    if current_user.is_authenticated:
        return "Already logged in"
    if (request.headers.get('Content-Type') == 'application/json'):
        try:
            user_info = request.get_json()
        except Exception:
            return "Wrong data format"
        user_pwd = user_info.get('password')
        hash_pwd = bcrypt.generate_password_hash(user_pwd).decode('utf-8')
        user_info['password'] = hash_pwd
        new_user = User(**user_info)
        storage.new(new_user)
        save_user = storage.save()
        if save_user is True:
            return 'User Created!'
        else:
            return 'Account with that email address exists already'
    return "Wrong content type"

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Function to update a user information"""
    from models import storage

    if (request.headers.get('Content-Type') == 'application/json'):
        try:
            user_info = request.get_json()
        except Exception:
            return "Wrong data format"
        user = storage.get('User', user_id)
        if not user:
            return "Invalid user id"
        for k, v, in user.items():
            v.update(**user_info)
            storage.new(v)
            save_user = storage.save()
        if save_user is True:
            return 'User Updated!'
        else:
            return 'Data must be unique'
    return 'Wrong content type'

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Function to delete a user"""
    from models import storage

    user = storage.get('User', user_id)
    if not user:
        return "Invalid user id"
    for k, v in user.items():
        storage.delete(v)
        storage.save()
    return "User Deleted!"