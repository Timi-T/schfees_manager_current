#!/usr/bin/python3
"""
Module to define the database model using SQLAlchemy
"""


from models.base_model import Base_model, Base
from models.fees import Fees
from models.users import User
from models.schools import School
from models.classrooms import Classroom
from models.students import Student
import sqlalchemy
from sqlalchemy import  create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

classes = {'User': User, 'School': School, 'Classroom': Classroom, 'Student': Student, 'Fees': Fees}

class DBstorage():
    """database storage class"""

    __engine = None
    __session = None

    def __init__(self):
        """Constructor method for database engine"""

        user = os.getenv('FEES_MAN_USER')
        pwd = os.getenv('FEES_MAN_PASSWORD')
        host = os.getenv('FEES_MAN_HOST')
        db_name = os.getenv('FEES_MAN_DBNAME')
        st = 'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db_name)
        self.__engine = create_engine(st, pool_pre_ping=True)

        if os.getenv('FEES_MAN_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Load objects from database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def new(self, obj):
        """Method to add new object to the current db session"""

        self.__session.add(obj)

    def save(self):
        """Method to save an object to current db session"""

        try:
            self.__session.commit()
            return True
        except Exception:
            return False

    def all(self, cls=None):
        """Return all objects in the database"""

        all_objs = {}
        new_dict = {}
        if cls is None:
            for cls_name, cls_obj in classes.items():
                new_objs = self.__session.query(cls_obj).all()
                for obj in new_objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            if cls in classes:
                new_objs = self.__session.query(classes[cls]).all()
            else:
                return None
            for obj in new_objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def delete(self, obj):
        """Delete object from database"""

        if obj:
            self.__session.delete(obj)

    def get(self, cls ,id):
        """Get an object using its id"""

        if id and cls:
            new_dict = {}
            all_cls = self.__session.query(classes.get(cls)).all()
            for obj in all_cls:
                if obj.id == id:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
                    return new_dict
        return None
        
    def filter_obj(self, cls, **attr):
        """Get a user by email"""

        if cls and attr:
            new_dict = {}
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                for k, v in attr.items():
                    if getattr(obj, k) == v:
                        key = obj.__class__.__name__ + '.' + obj.id
                        new_dict[key] = obj
                        return new_dict
            return new_dict
        return None

    def close(self):
        """close current sqlalchemy session"""
        self.__session.remove()