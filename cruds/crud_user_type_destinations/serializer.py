from backend import db
from . import models


class UserTypeDestinationsSerializer:

    def serialize(self, user_type_destinations):
        data=[]

        for user_type_destination in user_type_destinations:
            data.append(
            {'id': user_type_destination.id,
            'name':user_type_destination.name,
            'param_values_service':user_type_destination.param_values_service
            })

        return data
