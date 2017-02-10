from backend import db
from cruds.crud_course_type.models import CourseType


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(50))
    credits = db.Column(db.Integer)
    hours = db.Column(db.Integer)
    program_section = db.Column(db.Integer)
    course_type_id = db.Column(db.Integer, db.ForeignKey('course_type.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    course_sections = db.relationship('CourseSections', backref='course', lazy='dynamic')

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'credits':self.credits,
            'hours':self.hours,
            'program_section':self.program_section,
            'course_type_id':CourseType.query.get(self.course_type_id).serialize(),
            'program_id':self.program_id
        }

    def set_fields(self, fields):
        self.code = fields['code']
        self.name = fields['name']
        self.credits = fields['credits']
        self.hours = fields['hours']
        self.program_section = fields['program_section']
        self.course_type_id = fields['course_type_id']
        self.program_id = fields['program_id']
