#!/usr/bin/python3
"""
Module to define the Payment model.
Each Payment will have..
    - Unique ID
    - Payer name
    - student id
    - Amount
    - Purpose
It inherits from the base model to get its id and dates.
"""

from models.base_model import Base_model, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey


class Fees(Base_model, Base):
    """
    Class to define the Payment model
    """

    __tablename__ = 'fees'
    payer_name = Column(String(64), nullable=False)
    student_id = Column(String(64), ForeignKey('students.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    purpose = Column(String(128), nullable=False)

    def __init__(self, **kwargs):
        """constructor method for each payment"""
        super().__init__(**kwargs)