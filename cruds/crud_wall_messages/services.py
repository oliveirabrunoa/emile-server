from flask import jsonify, Blueprint, request
from . import models
from backend import db
from cruds.crud_user_type_destinations.models import UserTypeDestinations
from cruds.crud_user_type_destinations_user_type.models import UserTypeDestinationsUserType
from cruds.crud_user_type.models import UserType
from cruds.crud_wall_messages.models import WallMessages
import pytz
import datetime
import requests
import settings


wall_messages = Blueprint("wall_messages", __name__)


@wall_messages.route('/wall_messages/<user_id>', methods=['GET'])
def get_wall_messages(user_id):
    user = models.Users.query.get(user_id)
    messages = []
    today = datetime.date.today().toordinal()
    wall_messages_list = (db.session.query(models.WallMessages).
                                 filter(models.WallMessages.date >= datetime.date.fromordinal(today-14)).all())

    for message in wall_messages_list:
        users = set(message.get_destinations() + message.get_sender())

        if user in users:
            messages.append(message)

    return jsonify(wall_messages=[message.serialize() for message in messages]), 200


@wall_messages.route('/wall_push_notification', methods=['POST'])
def wall_push_notification():
    _dict = {}

    post_message = request.get_json()['post_message']
    user_type_destination_id = post_message['user_type_destination_id']
    parameter = post_message['parameter']
    message = post_message['message']
    sender = post_message['sender']

    today = datetime.datetime.now(tz=pytz.timezone('America/Bahia'))
    post_message['date'] = datetime.datetime.strftime(today,'%m-%d-%Y')
    wall_message = models.WallMessages()
    wall_message.set_fields(post_message)

    users = set(wall_message.get_destinations() + wall_message.get_sender())
    #send_notification

    db.session.add(wall_message)
    db.session.commit()

    return jsonify(wall_message=[message.serialize() for message in models.WallMessages.query.filter_by(sender=sender).all()]), 200


def send_message(token, device, body):
    try:
        post_data = dict(
            to=token,
            priority='high',
            notification=dict(
                    title=title,
                    body=body,
                    sound='Default',
            ),
        )
        json_data = json.dumps(post_data)
        headers = {
            'UserAgent': "FCM-Server",
            'Content-Type': 'application/json',
            'Authorization': 'key={}'.format(settings.PUSH_NOTIFICATIONS_SETTINGS['API_NOTIFICATION_KEY'])}

        response = requests.post(
            url=settings.PUSH_NOTIFICATIONS_SETTINGS['PUSH_NOTIFICATION_URL'],
            data=json_data, headers=headers)
        print(response)
        return True
    except Exception as e:
        print(e)
        return False
