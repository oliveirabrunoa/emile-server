from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def serialize(self):
        return {
            'username': self.username,
            'email': self.email
        }