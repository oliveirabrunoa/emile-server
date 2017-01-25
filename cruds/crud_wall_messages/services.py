from flask import jsonify, Blueprint, request
from . import models
from backend import db
from cruds.crud_user_type_destinations.models import UserTypeDestinations


wall_messages = Blueprint("wall_messages", __name__)


@wall_messages.route('/wall_push_notification', methods=['POST'])
def wall_push_notification():
    _dict = {}

    post_message = request.get_json()['post_message']
    user_type_destination_id = post_message['user_type_destination_id']
    parameter = post_message['parameter']
    message = post_message['message']

    query = UserTypeDestinations.query.filter_by(id=user_type_destination_id).first().users_query
    query = str(query).replace('$', str(parameter))
    exec(query, _dict)
    users = _dict['users']

    return jsonify(users=[user.serialize() for user in set(users)]), 200
