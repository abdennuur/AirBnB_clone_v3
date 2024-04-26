#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """
        Handles long term storage of all class instances
    """
    CLS_NAMES_CLASSES = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CLS_NAMES_CLASSES - This dictionary contains class names as keys and their corresponding classes as values."""

    FILE_PATH = './dev/file.json'
    """FILE_PATH - This variable holds the path to the JSON file used for storage."""

    OBJECTS = {}
    """OBJECTS - This dictionary holds all the objects stored in memory."""

    def all(self, cls=None):
        """
        Returns private attribute: OBJECTS
        """
        if cls is not None:
            new_objs = {}
            for obj_key, obj in FileStorage.OBJECTS.items():
                if type(obj).__name__ == cls:
                    new_objs[obj_key] = obj
            return new_objs
        else:
            return FileStorage.OBJECTS

    def new(self, obj):
        """
        Sets / updates in OBJECTS the obj with key <obj class name>.id
        """
        obj_key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.OBJECTS[obj_key] = obj

    def save(self):
        """
        Serializes OBJECTS to the JSON file (path: FILE_PATH)
        """
        fname = FileStorage.FILE_PATH
        storage_dict = {}
        for obj_key, obj in FileStorage.OBJECTS.items():
            storage_dict[obj_key] = obj.to_json(saving_file_storage=True)
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(storage_dict, f_io)

    def reload(self):
        """
        If file exists, deserializes JSON file to OBJECTS, else nothing
        """
        fname = FileStorage.FILE_PATH
        FileStorage.OBJECTS = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except:
            return
        for obj_id, obj_dict in new_objs.items():
            cls_name = obj_dict['__class__']
            FileStorage.OBJECTS[obj_id] = FileStorage.CLS_NAMES_CLASSES[cls_name](**obj_dict)

    def delete(self, obj=None):
        """
        Deletes obj from OBJECTS if it's inside
        """
        if obj:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(obj_key):
                del FileStorage.OBJECTS[obj_key]
            self.save()

    def delete_all(self):
        """
        Deletes all stored objects, for testing purposes
        """
        try:
            with open(FileStorage.FILE_PATH, mode='w') as f_io:
                pass
        except:
            pass
        del FileStorage.OBJECTS
        FileStorage.OBJECTS = {}
        self.save()

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one object based on class name and id
        """
        if cls and id:
            obj_key = "{}.{}".format(cls, id)
            all_objs = self.all(cls)
            return all_objs.get(obj_key)
        return None

    def count(self, cls=None):
        """
        Count of all objects in storage
        """
        return len(self.all(cls))

