#!/usr/bin/python3
"""
Module to define the Student model.
Each Student will have..
    - Unique ID
    - student id
    - Student name
    - Class name
    - Class id
    - Fees paid in total
    - School id
    - Parent phone no
It inherits from the base model to get its id and dates.
"""

from models.base_model import Base_model, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Student(Base_model, Base):
    """
    Class to define the Student model
    """

    __stu_id = 1010

    __tablename__ = 'students'
    stu_id = Column(String(64), nullable=False)
    name = Column(String(64), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    sex = Column(String(32), nullable=False)
    cls = Column(String(32), nullable=False)
    cls_id = Column(String(64), ForeignKey('classrooms.id'), nullable=False)
    sch_id = Column(String(64), ForeignKey('schools.id'), nullable=False)
    fees_paid = Column(Integer, default=0)
    parent_phone = Column(String(32), nullable=True)
    fees = relationship("Fees", backref="students", cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        """constructor method for each student"""
        super().__init__(**kwargs)
        self.stu_id = str(Student.__stu_id)
        self.fees_paid = 0
        Student.__stu_id += 1