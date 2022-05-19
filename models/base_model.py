#!/usr/bin/python3
"""
Module that defines base model.
All other models;
    - School
    - Class
    - Student
    - User
     - Fees
        would inherit from this model thier;
            - ID
            - Date created
            - Date updated
"""

from datetime import datetime
from time import strftime, strptime
import uuid
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Base_model():
    """
    Base model class
    """

    id = Column(String(60), primary_key=True)
    date_created = Column(String(30), default=datetime.utcnow)
    date_updated = Column(String(30), default=datetime.utcnow)

    def __init__(self, **kwargs):
        """Constructor method for each model"""
        from models import storage

        if (kwargs):
            for k, v in kwargs.items():
                if k != __class__:
                    setattr(self, k, v)
            if not kwargs.get('date_created'):
                self.date_created = datetime.utcnow()
            if not kwargs.get('date_updated'):
                self.date_updated = datetime.utcnow()
            else:
                self.date_updated = datetime.utcnow()
            if not kwargs.get('id'):
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.date_created = datetime.utcnow()
            self.date_updated = datetime.utcnow()
        storage.new(self)

    def to_dict(self):
        """Method to get the dictionary representation of an object"""
        
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        if new_dict.get('_sa_instance_state'):
            del new_dict['_sa_instance_state']
        if new_dict.get('date_created'):
            d = new_dict['date_created']
        if new_dict.get('date_updated'):
            d = new_dict['date_updated']
        return new_dict

    def update(self, **kwargs):
        """Function to update attributes of an instance"""
        from models import storage

        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
            setattr(self, 'date_updated', datetime.utcnow())
            #storage.new(self)