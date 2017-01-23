import datetime
from backend import db
from cruds.crud_user_type.models import UserType


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(250))
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String(1))
    address = db.Column(db.String(250))
    type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    course_sections = db.relationship('CourseSectionStudents', cascade="save-update, merge, delete")

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'birth_date': datetime.date.strftime(self.birth_date, "%m-%d-%Y"),
            'gender': self.gender,
            'address': self.address,
            'type': UserType.query.filter_by(id=self.type).first().serialize(),
        }

    def set_fields(self, fields):
        self.username = fields['username']
        self.email = fields['email']
        self.name = fields['name']
        self.birth_date = fields['birth_date']
        self.gender = fields['gender']
        self.address = fields['address']
        self.birth_date = datetime.datetime.strptime(fields['birth_date'], "%m-%d-%Y").date()
        self.type = fields['type']
