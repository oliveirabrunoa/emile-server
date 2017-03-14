import datetime
from backend import db
from cruds.crud_user_type.models import UserType
from cruds.crud_program.models import Program
import os
import settings
import requests
import random
from flask import jsonify


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(250))
    birth_date = db.Column(db.Date())
    gender = db.Column(db.String(1))
    address = db.Column(db.String(250))
    push_notification_token = db.Column(db.Text(), nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=True)
    image_path = db.Column(db.Text(), nullable=True)
    course_sections = db.relationship('CourseSectionStudents', cascade="save-update, merge, delete")

    def serialize(self):

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'birth_date': datetime.date.strftime(self.birth_date, "%m-%d-%Y") if self.birth_date  else self.birth_date,
            'gender': self.gender,
            'address': self.address,
            'program_id': self.program_id,
            'push_notification_token': self.push_notification_token,
            'type': UserType.query.filter_by(id=self.type).first().serialize(),
            'image_path': self.image_path,
        }

    def set_fields(self, fields):
        self.username = fields['username']
        self.email = fields['email']
        self.password = fields['password']
        self.name = fields['name']
        self.gender = fields['gender']
        self.address = fields['address']
        self.birth_date = datetime.datetime.strptime(fields['birth_date'], "%m-%d-%Y").date() if self.birth_date  else self.birth_date
        self.program_id = fields['program_id']
        self.type = fields['type']

    def save_image(self, file):
        file_name, _format = str(file.filename).rsplit('.', 1)

        if not _format in settings.ALLOWED_EXTENSIONS:
            _format = 'jpg'

        files = {'image_file': file}
        headers = {
            "enctype": "multipart/form-data"
        }

        r = requests.post('http://eliakimdjango.pythonanywhere.com/save_profile_image',
                          files={'file': (self.username + str(random.randint(1000, 10000)) + '.' + _format, file,
                          headers, {'Expires': '0'})},
                          data={'old_file_path': self.image_path})
        # r = requests.post('http://127.0.0.1:2000/save_profile_image',
        #                   files={'file': (self.username + str(random.randint(1000, 10000)) + '.' + _format, file,
        #                                   headers, {'Expires': '0'})},
        #                   data={'old_file_path': self.image_path})
        if r.status_code==200:
            self.image_path = r.json()['result']
            return True
