import datetime
from backend import db
from cruds.crud_user_type.models import UserType
from cruds.crud_users.models import Users
from cruds.crud_user_type_destinations.models import UserTypeDestinations


class WallMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date())
    sender = db.Column(db.Integer, db.ForeignKey("users.id"))
    destination = db.Column(db.Integer, db.ForeignKey("user_type_destinations.id"))
    message = db.Column(db.String(140))

    def serialize(self):
        return {
            'id': self.id,
            'date': datetime.date.strftime(self.date, "%m-%d-%Y"),
            'sender': self.sender,
            'destination': self.destination,
            'message': self.message
        }

    def set_fields(self, fields):
        self.date = datetime.datetime.strptime(fields['date'], "%m-%d-%Y").date()
        self.sender = fields['sender']
        self.destination = fields['destination']
        self.message = fields['message']
