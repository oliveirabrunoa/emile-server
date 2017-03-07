from csv_loader import CSVLoader
from cruds.crud_user_type.models import UserType


class UserTypeLoader(CSVLoader):

    def create_object(self, row):
        user_type_class = self.import_relative_path('cruds.crud_user_type.models.UserType')

        obj = user_type_class()

        user_type = self.session.query(UserType).get(row[0])

        if user_type:
            return

        obj.id = row[0]
        obj.name = row[1]

        return obj

    def file_name(self):
        return 'user_type.csv'
