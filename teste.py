import register_blueprints
import backend
import os
import unittest
from flask import Flask
from pathlib import Path
import json


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    app = None
    app_client = None

    # executed before all tests in the class
    @classmethod
    def setUpClass(cls):
        os.environ["DATABASE_URL"] = "sqlite:///test.db"
        os.environ["APP_SETTINGS"] = "config.TestingConfig"

        cls.app = cls.create_app()
        register_blueprints.register_blueprints(cls.app)
        cls.app_client = cls.app.test_client()

        my_file = Path(os.path.join(os.path.dirname(__file__), 'test.db'))

        with cls.app.app_context():
            if my_file.is_file():
                backend.db.drop_all()
            backend.db.create_all()

    # executed after all tests in the class
    @classmethod
    def tearDownClass(cls):
        os.environ["APP_SETTINGS"] = "config.DevelopmentConfig"
        with cls.app.app_context():
            backend.db.session.remove()
            backend.db.drop_all()

    @staticmethod
    def create_app():
        app = Flask("teste")

        app.config.from_object(os.environ['APP_SETTINGS'])
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        backend.db.init_app(app)
        return app

    def test_users(self):
        response = self.app_client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        user = dict(username='eliakincosta', email='eliakim170@gmail.com',
                    name='Eliakin Costa', gender='M',
                    address='Rua Teste', birth_date='11-12-1993',
                    type='student')
        response = self.app_client.post('/add_user',
                                        data=json.dumps(user),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
