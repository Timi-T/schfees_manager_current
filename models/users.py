#!/usr/bin/python3
"""
Module to define the User/Admin model.
Each User will have..
    - Unique ID
    - Number of Schools
    - Email addr
    - Password
    - Phone number
It inherits from the base model to get its id and dates.
"""


import sqlalchemy
from models.base_model import Base_model, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from api.v1.app import login_manager


@login_manager.user_loader
def load_user(user_id):
    from models import storage
    """Function to load a user for login session"""
    
    user_dict = storage.get('User', user_id)
    for k, user in user_dict.items():
        return user

class User(Base_model, Base, UserMixin):
    """
    Class to define the User model
    """

    __tablename__ = 'users'
    email = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    name = Column(String(128), nullable=False)
    phone_no = Column(String(32), nullable=True)
    schools = relationship("School", backref="users", cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """constructor method for each user/admin"""
        super().__init__(**kwargs)