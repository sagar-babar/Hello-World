import os
import json
import sqlite3
import unittest

from api._user_data import app as app_step_1

CREATE_USER_TABLE_QUERY = """
create table users (
    id integer primary key autoincrement,
    user text not null,
    dob text not null
);
"""
TESTING_DATABASE_NAME = 'test_user.db'


class BaseDatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_step_1.config.update({
            'DATABASE_NAME': TESTING_DATABASE_NAME
        })
        cls.db = sqlite3.connect(TESTING_DATABASE_NAME)
        cls.db.execute(CREATE_USER_TABLE_QUERY)
        cls.db.commit()

    @classmethod
    def tearDownClass(cls):
        os.remove(TESTING_DATABASE_NAME)

    def setUp(self):
        self.app = self.APP.test_client()
        self.db.execute("DELETE FROM users;")
        self.db.commit()


class Step1TestCase(BaseDatabaseTestCase):
    APP = app_step_1
    def test_user_creation_correct_parameters(self):
        # Preconditions
        resp = self.app.get('/hello/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 0)
        # Test
        put_data = {
            'dateOfBirth' : '2006-06-17'
        }
        resp = self.app.put('/hello/sagar',
                             data=json.dumps(put_data),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.content_type, 'application/json')

        # Postconditions
        resp = self.app.get('/hello/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 1)

        # Postcondtion: users correct ID incremented
        ulysses = content[0]

        self.assertEqual(ulysses, {
            'id1': 1,
            'user': 'sagar',
            'dob': "2006-06-17"
        })


    def test_user_creation_incorrect_parameters(self):
        # Forget the dob argument
        put_data = {
            'dateOfBirt' : '2006-06-17'
        }
        resp = self.app.put('/hello/sagar',
                             data=json.dumps(put_data),
                             content_type='application/json')

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('dateOfBirth' in resp.get_data(as_text=True))

    def test_user_creation_incorrect_content_type(self):
        # incorrect content type argument
        put_data = {
            'dateOfBirth' : '2006-06-17'
        }

        resp = self.app.put('/hello/sagar',
                             data=json.dumps(put_data))

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('Content Type' in resp.get_data(as_text=True))
