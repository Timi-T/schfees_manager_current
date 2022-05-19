#!/usr/bin/python3
"""
Define all api route functions for the user
"""


from flask_bcrypt import Bcrypt
from api.v1.views import app_views
from flask import request, render_template
import json
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint, flash, redirect, url_for



bcrypt = Bcrypt()

auth = Blueprint('auth', __name__, url_prefix='/')

@auth.route('/home', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def home():
    """Return user to home page"""

    return render_template('home.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def log_in():
    """Function to login a user"""
    from models import storage

    if request.method == "POST":
        info = request.form
        user_info = {}
        for k, v in info.items():
            user_info[k] = v
        user = storage.filter_obj('User', **{"email": user_info['email']})
        user_pwd = user_info.get('login_password')
        if not user:
            flash('Invalid Username/Password', category='error')
            return render_template('login.html')
        for k, usr in user.items():
            check_user = bcrypt.check_password_hash(usr.password, user_pwd)
        if check_user:
            login_user(usr, remember=True)
            return redirect(url_for('auth.home'))
        else:
            flash('Invalid Username/Password', category='error')
    return render_template('login.html')

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Function to sign in a user"""
    from models import storage
    from models.users import User

    if request.method == 'POST':
        info = request.form
        user_info = {}
        for k, v in info.items():
            user_info[k] = v
        name = user_info.get('name')
        email = user_info.get('email')
        phone_no = user_info.get('phone_no')
        password = user_info.get('password1')
        confirm_pwd = user_info.get('password2')
        if len(name) < 4:
            flash('Name must be greater than 4 characters', category='error')
        elif len(phone_no) < 11:
            flash('Enter a valid phone number', category='error')
        elif password != confirm_pwd:
            flash('Passwords do not match', category='error')
        elif len(password) < 5:
            flash('Password too short', category='error')
        else:
            check_user = storage.filter_obj('User', **{"email": email})
            if check_user:
                flash('Account already exists', category='error')
                return render_template('sign_up.html')
            user_pwd = user_info.get('password1')
            hash_pwd = bcrypt.generate_password_hash(user_pwd).decode('utf-8')
            user_info['password'] = hash_pwd
            new_user = User(**user_info)
            storage.new(new_user)
            save_user = storage.save()
            if save_user is True:
                flash('Sign up successful!', category='success')
                return redirect(url_for('auth.log_in'))
            else:
                flash('Error creating account', category='error')
                return render_template('sign_up.html')
    return render_template('sign_up.html')

@auth.route('/logout', strict_slashes=False)
@login_required
def logout():
    """Function to logout a user"""

    logout_user()
    flash('Logged out successful!', category='success')
    return render_template('login.html')