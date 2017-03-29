from backend import db
from . import models
from cruds.crud_users.models import Users
import datetime
from cruds.crud_users.serializer import UsersSerializer


class WallMessagesSerializer:

    def serialize(self, messages):
        data=[]

        for message in messages:
            sender =UsersSerializer().serialize([Users.query.get(message.sender)])
            data.append(
            {'id': message.id,
            'date': message.date,
            'sender': dict(id=sender['id'], name=sender['name'],email=sender['email'],program_id=sender['program_id'], type=sender['type']),
            #'user_type_destination_id': message.destination,
            'message': message.message
            })

        return data
