from backend import db
from . import models
from cruds.crud_courses.models import Courses
from cruds.crud_course_section_students.models import CourseSectionStudents
from cruds.crud_course_sections.models import CourseSections
from sqlalchemy import or_, func
import importlib

class Manager:

    def course_times_by_student(self, course, student):
        return (db.session.query(func.count(CourseSectionStudents.id)).
                                        filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                        filter(CourseSections.course_id == Courses.id).
                                        filter(Courses.program_id == models.Program.id).
                                        filter(models.Program.id == student.program_id).
                                        filter(CourseSectionStudents.user_id == student.id).
                                        filter(Courses.id == course.id).
                                        filter(or_ (CourseSectionStudents.status == 2,
                                                    CourseSectionStudents.status == 3)).
                                        group_by(Courses.code,Courses.program_section).order_by(Courses.program_section).first())
