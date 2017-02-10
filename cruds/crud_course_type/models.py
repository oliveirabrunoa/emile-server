from backend import db


class CourseType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description
        }

    def set_fields(self, fields):
        self.description = fields['description']
