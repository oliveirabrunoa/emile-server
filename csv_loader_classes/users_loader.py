from csv_loader import CSVLoader
from cruds.crud_user_type.models import UserType
from cruds.crud_program.models import Program
from cruds.crud_users.models import Users
import datetime


class UsersLoader(CSVLoader):

    def create_object(self, row):
        users_class = self.import_relative_path('cruds.crud_users.models.Users')

        obj = users_class()

        user = self.session.query(Users).get(row[0])

        if user:
            return

        birth_date = datetime.datetime.strptime(row[5], "%d-%m-%Y").date()
        user_type_id = self.session.query(UserType).filter(UserType.name==row[8]).first().id
        program_id = self.session.query(Program).filter(Program.abbreviation==row[9]).first().id

        obj.id = row[0]
        obj.username = row[1]
        obj.email = row[2]
        obj.password = row[3]
        obj.name = row[4]
        obj.birth_date = birth_date
        obj.gender = row[6]
        obj.address = row[7]
        obj.type = user_type_id
        obj.program_id = program_id

        return obj

    def file_name(self):
        return 'users.csv'
