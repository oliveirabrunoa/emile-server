from csv_loader import CSVLoader
from cruds.crud_course_type.models import CourseType
import datetime


class CourseTypeLoader(CSVLoader):

    def create_object(self, row):
        course_type_class = self.import_relative_path('cruds.crud_course_type.models.CourseType')

        obj = course_type_class()

        course_type = self.session.query(CourseType).get(row[0])

        if course_type:
            return

        obj.id = row[0]
        obj.name = row[1]

        return obj

    def file_name(self):
        return 'course_type.csv'
