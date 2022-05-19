#!/usr/bin/python3
"""
Initialize a database session when the models package is initialized
"""
from models.engine.db_storage import DBstorage


storage = DBstorage()
storage.reload()