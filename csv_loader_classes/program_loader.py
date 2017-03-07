from csv_loader import CSVLoader
from cruds.crud_program.models import Program


class ProgramLoader(CSVLoader):

    def create_object(self, row):
        program_class = self.import_relative_path('cruds.crud_program.models.Program')

        obj = program_class()

        program = self.session.query(Program).get(row[0])

        if program:
            return

        obj.id = row[0]
        obj.name = row[1]
        obj.abbreviation = row[2]
        obj.total_hours = row[3]
        obj.total_credits = row[4]

        return obj

    def file_name(self):
        return 'program.csv'
