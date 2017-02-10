from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_course_section_students_status.models import CourseSectionStudentsStatus


class CourseSectionStudents(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    course_section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_section = db.relationship("CourseSections")
    status = db.Column(db.Integer, db.ForeignKey('course_section_students_status.id'), nullable=False)
    grade = db.Column(db.Float, nullable=True)

    def serialize(self):
        return {
            'course_section_id': self.course_section_id,
            'user_id': self.user_id,
            'status': CourseSectionStudentsStatus.query.get(self.status).serialize(),
            'grade': self.grade
        }

    def set_fields(self, fields):
        self.course_section_id = fields['course_section_id']
        self.user_id = fields['user_id']
        self.status = fields['status']
        self.grade = fields['grade']
