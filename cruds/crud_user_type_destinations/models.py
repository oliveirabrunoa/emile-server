import datetime
from backend import db
from cruds.crud_user_type.models import UserType


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)


    def serialize(self):
        return {
            'id': self.id,
        }

    def set_fields(self, fields):
        self.id = fields['username']
        self.birth_date = datetime.datetime.strptime(fields['birth_date'], "%m-%d-%Y").date()
        
