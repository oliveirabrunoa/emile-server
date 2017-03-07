from csv_loader import CSVLoader
from cruds.crud_course_section_students_status.models import CourseSectionStudentsStatus
import datetime


class CourseSectionStudentsStatusLoader(CSVLoader):

    def create_object(self, row):
        course_section_students_status_class = self.import_relative_path('cruds.crud_course_section_students_status.models.CourseSectionStudentsStatus')

        obj = course_section_students_status_class()

        course_section_students_status = self.session.query(CourseSectionStudentsStatus).get(row[0])

        if course_section_students_status:
            return

        obj.id = row[0]
        obj.name = row[1]

        return obj

    def file_name(self):
        return 'course_section_students_status.csv'
