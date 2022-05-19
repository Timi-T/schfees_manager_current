#!/usr/bin/python3
"""
Module to define the classroom model.
Each classroom will have..
    - Unique ID
    - Class name
    - Number of students
    - Fees paid in total
    - Name of class teacher
It inherits from the base model to get its id and dates.
"""

from models.base_model import Base_model, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Classroom(Base_model, Base):
    """
    Class to define the Classroom model
    """

    __tablename__ = 'classrooms'
    name = Column(String(64), nullable=False)
    sch_id = Column(String(64), ForeignKey('schools.id'), nullable=False)
    no_of_students = Column(Integer, default=0)
    fees_paid = Column(Integer, default=0)
    fees_expected = Column(Integer, default=0)
    class_teacher = Column(String(64), nullable=True)
    students_list = '[]'
    students = relationship("Student", backref="classrooms", cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """constructor method for each class"""
        super().__init__(**kwargs)
        self.no_of_students = 0
        self.fees_paid = 0
        self.students_list = []