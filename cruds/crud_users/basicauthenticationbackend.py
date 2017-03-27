from . import models
from flask import jsonify
from cruds.crud_program.models import Program
from cruds.crud_user_type.models import UserType


class BasicAuthenticationBackend:

    def authenticate(self, email, password):
        user = models.Users.query.filter_by(email=email, password=password).first()
        if user:
            user_type = UserType.query.get(user.type)
            program = Program.query.get(user.program_id)
            return jsonify(user=dict(user.serialize(), type=user_type.serialize(),program_id=dict(id=program.id, abbreviation=program.abbreviation, name=program.name))), 200
        else:
            return jsonify(result='Invalid email or password'), 404
