from . import models
from flask import jsonify


class BasicAuthenticationBackend:

    def authenticate(self, email, password):
        user = models.Users.query.filter_by(email=email, password=password).first()
        if user:
            return jsonify(user=user.serialize()), 200
        else:
            return jsonify(result='Invalid email or password'), 404
