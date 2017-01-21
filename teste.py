import register_blueprints
import backend
import os
import unittest
from flask import Flask
from pathlib import Path
import json


TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        os.environ["DATABASE_URL"] = "sqlite:///test.db"
        os.environ["APP_SETTINGS"] = "config.TestingConfig"

        self.app = self.create_app()
        register_blueprints.register_blueprints(self.app)
        self.app_client = self.app.test_client()

        my_file = Path(os.path.join(os.path.dirname(__file__), 'test.db'))

        with self.app.app_context():
            if my_file.is_file():
                backend.db.drop_all()
            backend.db.create_all()

    # executed after each test
    def tearDown(self):
        os.environ["APP_SETTINGS"] = "config.DevelopmentConfig"
        with self.app.app_context():
            backend.db.session.remove()
            backend.db.drop_all()

    def create_app(self):
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
