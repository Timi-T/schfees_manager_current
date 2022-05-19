#!/usr/bin/python3
"""
Module to define the School model.
Each School will have..
    - Unique ID
    - School name
    - Number of students
    - Number of classes
    - Fees paid in total
It inherits from the base model to get its id and dates.
"""

from models.base_model import Base_model, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


class School(Base_model, Base):
    """
    Class to define the School model
    """

    __tablename__ = 'schools'
    name = Column(String(128), nullable=False)
    address = Column(String(256), nullable=False)
    user_id = Column(String(64), ForeignKey('users.id'))
    no_of_students = Column(Integer, default=0)
    no_of_classes = Column(Integer, default=0)
    fees_paid = Column(Integer, default=0)
    level = Column(String(32), nullable=False)
    classes = relationship('Classroom', backref='schools', cascade='all, delete, delete-orphan')
    students = relationship('Student', backref='schools', cascade='all, delete, delete-orphan')

    def __init__(self, name, address, **kwargs):
        """constructor method for each class"""
        super().__init__(**kwargs)
        self.name = name
        self.address = address
        self.no_of_students = 0
        self.no_of_classes = 0
        self.fees_paid = 0
