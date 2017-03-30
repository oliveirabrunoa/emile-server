from backend import db


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def set_fields(self, fields):
        self.name = fields['name']
