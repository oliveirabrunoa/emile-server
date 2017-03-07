from csv_loader import CSVLoader


class UsersLoader(CSVLoader):

    def create_object(self, row):
        users_class = self.import_relative_path('cruds.crud_users.models.Users')
