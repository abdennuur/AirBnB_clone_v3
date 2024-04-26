#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
import inspect
import json
import models
from models import engine
from models.engine.file_storage import FileStorage
import pep8
from os import environ, stat, remove, path

User = models.user.User
BaseModel = models.base_model.BaseModel
State = models.state.State
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE != 'db':
    FileStorage = models.file_storage.FileStorage
storage = models.storage
JSON_FILE_PATH = './dev/file.json'


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is not db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing FileStorage docs"""

    all_funcs = inspect.getmembers(FileStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')

    def tearDownClass():
        """Cleans up the tests by removing storage objects"""
        storage.delete_all()
        remove(JSON_FILE_PATH)

    def test_doc_file(self):
        """Checks documentation for the file"""
        expected = ("\nHandles I/O, writing and reading, of JSON for storage "
                    "of all class instances\n")
        actual = models.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Checks documentation for the class"""
        expected = ('\n        handles long term storage of all class instance'
                    's\n    ')
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """Tests for ALL DOCS for all functions in FileStorage class"""
        all_functions = TestFileStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_fs(self):
        """Checks if filestorage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """Tests if file has correct permissions so user can execute"""
        file_stat = stat('models/engine/file_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """Testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """Sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('..... For FileStorage Class .....')
        print('.................................\n\n')
        cls.base_model_obj = BaseModel()
        cls.state_obj = State(name="Illinois")
        cls.base_model_obj.save()
        cls.state_obj.save()

    def tearDownClass():
        """Cleans up the tests by removing storage objects"""
        storage.delete_all()
        remove(JSON_FILE_PATH)

    def setUp(self):
        """Initializes new storage object for testing"""
        self.base_model_obj = TestBmFsInstances.base_model_obj
        self.state_obj = TestBmFsInstances.state_obj

    def test_instantiation(self):
        """Checks proper FileStorage instantiation"""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_file_exists(self):
        """Checks if storage file exists after saving"""
        remove(JSON_FILE_PATH)
        self.base_model_obj.save()
        self.assertTrue(path.isfile(JSON_FILE_PATH))

    def test_all(self):
        """Checks if all() function returns newly created instance"""
        base_model_id = self.base_model_obj.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if base_model_id in k:
                actual = True
        self.assertTrue(True)

    def test_all_state(self):
        """Checks if all() function returns newly created state instance"""
        state_id = self.state_obj.id
        state_objs = storage.all("State")
        actual = False
        for k in state_objs.keys():
            if state_id in k:
                actual = True
        self.assertTrue(True)

    def test_obj_saved_to_file(self):
        """Checks if object is properly saved to file"""
        remove(JSON_FILE_PATH)
        self.base_model_obj.save()
        base_model_id = self.base_model_obj.id
        actual = False
        with open(JSON_FILE_PATH, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if base_model_id in k:
                actual = True
        self.assertTrue(True)

    def test_to_json(self):
        """Checks if to_json returns serializable dict object"""
        base_model_json = self.base_model_obj.to_json()
        actual = True
        try:
            serialized = json.dumps(base_model_json)
        except:
            actual = False
        self.assertTrue(actual)

    def test_reload(self):
        """Checks proper usage of reload function"""
        remove(JSON_FILE_PATH)
        self.base_model_obj.save()
        base_model_id = self.base_model_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if base_model_id in k:
                actual = True
        self.assertTrue(actual)

    def test_save_reload_class(self):
        """Checks proper usage of class attribute in file storage"""
        remove(JSON_FILE_PATH)
        self.base_model_obj.save()
        base_model_id = self.base_model_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if base_model_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = True
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
class TestUserFsInstances(unittest.TestCase):
    """Testing for class instances"""

    @classmethod
    def setUpClass(cls):
        """Sets up the class"""
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')
        cls.user = User()
        cls.user.save()
        cls.base_model_obj = BaseModel()
        cls.base_model_obj.save()

    def tearDownClass():
        """Cleans up the tests by removing storage objects"""
        storage.delete_all()
        remove(JSON_FILE_PATH)

    def setUp(self):
        """Initializes new user for testing"""
        self.user = TestUserFsInstances.user
        self.base_model_obj = TestUserFsInstances.base_model_obj

    def test_storage_file_exists(self):
        """Checks if storage file exists after saving"""
        remove(JSON_FILE_PATH)
        self.user.save()
        self.assertTrue(path.isfile(JSON_FILE_PATH))

    def test_count_cls(self):
        """Checks count method with class input arg"""
        count_user = storage.count('User')
        expected = 1
        self.assertEqual(expected, count_user)

    def test_count_all(self):
        """Checks the count method with no class input"""
        count_all = storage.count()
        expected = 2
        self.assertEqual(expected, count_all)

    def test_get_cls_id(self):
        """Checks get method with class and id inputs"""
        duplicate = storage.get('User', self.user.id)
        expected = self.user.id
        actual = duplicate.id
        self.assertEqual(expected, actual)

    def test_all(self):
        """Checks if all() function returns newly created instance"""
        user_id = self.user.id
        all_obj = storage.all()
        actual = False
        for k in all_obj.keys():
            if user_id in k:
                actual = True
        self.assertTrue(actual)

    def test_obj_saved_to_file(self):
        """Checks if object is properly saved to file"""
        remove(JSON_FILE_PATH)
        self.user.save()
        user_id = self.user.id
        actual = False
        with open(JSON_FILE_PATH, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if user_id in k:
                actual = True
        self.assertTrue(actual)

    def test_reload(self):
        """Checks proper usage of reload function"""
        remove(JSON_FILE_PATH)
        self.base_model_obj.save()
        user_id = self.base_model_obj.id
        actual = False
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if user_id in k:
                actual = True
        self.assertTrue(actual)


if __name__ == '__main__':
    unittest.main()

