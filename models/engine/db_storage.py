#!/usr/bin/python3
"""
Database Engine Implementation using SQLAlchemy
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import amenity, city, place, review, state, user


class DBStorage:
    """
    Handles long-term storage of all class instances using a relational database.
    """

    # Class Name Constants
    CLASS_NAMES = {
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    # Database Engine and Session Initialization
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the database engine.
        """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve all objects of a specific class or all objects if no class is specified.
        """
        obj_dict = {}
        if cls is not None:
            query = self.__session.query(DBStorage.CLASS_NAMES[cls])
            for obj in query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

        for c in DBStorage.CLASS_NAMES.values():
            query = self.__session.query(c)
            for obj in query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
        return obj_dict

    def new(self, obj):
        """
        Add a new object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def rollback_session(self):
        """
        Rollback a session in the event of an exception.
        """
        self.__session.rollback()

    def delete(self, obj=None):
        """
        Delete an object from the current database session.
        """
        if obj:
            self.__session.delete(obj)
            self.save()

    def delete_all(self):
        """
        Delete all stored objects from the database (for testing purposes).
        """
        for c in DBStorage.CLASS_NAMES.values():
            query = self.__session.query(c)
            all_objs = [obj for obj in query]
            for obj in range(len(all_objs)):
                to_delete = all_objs.pop(0)
                to_delete.delete()
        self.save()

    def reload(self):
        """
        Reload all tables in the database schema and session from the engine.
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
        Close the current database session.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieve one object based on class name and id.
        """
        if cls and id:
            fetch = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
        Return the count of all objects in storage.
        """
        return len(self.all(cls))

