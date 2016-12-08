import datetime
from backend import db


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classes_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    lesson_start_date = db.Column(db.DateTime())
    lesson_finish_date = db.Column(db.DateTime())


    def serialize(self):
        return {
            'id': self.id,
            'lesson_start_date': datetime.date.strftime(self.lesson_start_date, "%m-%d-%Y %H:%M:%S"),
            'lesson_finish_date': datetime.date.strftime(self.lesson_finish_date, "%m-%d-%Y %H:%M:%S"),
            'classes': self.classes_lesson.serialize(),
        }

    def set_fields(self, fields):
        self.classes_id = fields['classes_id']
        self.lesson_start_date = fields['lesson_start_date']
        self.lesson_finish_date = fields['lesson_finish_date']