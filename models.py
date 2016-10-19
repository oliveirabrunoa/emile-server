from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(250))
    birth_date = db.Column(db.String(20))
    gender = db.Column(db.String(1))
    address = db.Column(db.String(250))

    def __init__(self, username='', email=''):
        self.username = username
        self.email = email

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'address': self.address
        }
