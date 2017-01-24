import datetime
from backend import db
from cruds.crud_user_type.models import UserType


class UserTypeDestinations(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    param_values_service = db.Column(db.String(250))
    users_query  = db.Column(db.String(250))


    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'param_values_service':self.param_values_service,
            'users_query': self.users_query
        }

    def set_fields(self, fields):
        self.name = fields['name']
        self.param_values_service = fields['param_values_service']
        self.users_query = fields['users_query']
