from backend import db
from cruds.crud_courses.models import Courses


class CourseSectionStudents(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    course_section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_section = db.relationship("CourseSections")
    __table_args__ = (db.UniqueConstraint('course_section_id','user_id', name='course_section_user_uc'),)

    def serialize(self):
        return {
            'course_section_id': self.course_section_id,
            'user_id': self.user_id,
        }

    def set_fields(self, fields):
        self.course_section_id = fields['course_section_id']
        self.user_id = fields['user_id']
