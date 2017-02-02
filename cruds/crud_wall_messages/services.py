from flask import jsonify, Blueprint, request
from . import models
from backend import db
from cruds.crud_user_type_destinations.models import UserTypeDestinations
import pytz
import datetime
import requests
import settings


wall_messages = Blueprint("wall_messages", __name__)


@wall_messages.route('/wall_push_notification', methods=['POST'])
def wall_push_notification():
    _dict = {}

    post_message = request.get_json()['post_message']
    user_type_destination_id = post_message['user_type_destination_id']
    parameter = post_message['parameter']
    message = post_message['message']
    sender = post_message['sender']

    query = UserTypeDestinations.query.filter_by(id=user_type_destination_id).first().users_query
    query = str(query).replace('$', str(parameter))
    exec(query, _dict)
    users = _dict['users']
    send_message([user.push_notification_token for user in users], message)

    today = datetime.datetime.now(tz=pytz.timezone('America/Bahia'))
    post_message['date'] = datetime.datetime.strftime(today,'%m-%d-%Y')
    wall_message = models.WallMessages()
    wall_message.set_fields(post_message)

    db.session.add(wall_message)
    db.session.commit()

    return jsonify(wall_message=[message.serialize() for message in models.WallMessages.query.filter_by(sender=sender).all()]), 200


def send_message(users_tokens, body):
    try:
        registration_ids = users_tokens
        message_title = 'Nova mensagem do Émile'
        message_body = body
        result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
        return True
    except Exception as e:
        return False
