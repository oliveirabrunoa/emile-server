from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_user.models import User


classes = Blueprint("turma", __name__)


@classes.route('/classes', methods=['GET'])
def get_classes():
    return jsonify(classes=[dict(id=classes.id, code=classes.code) for classes in models.Classes.query.all()])


@classes.route('/add_classes', methods=['POST'])
def add_classes():
    """ This method it was implemented considering that all fields are required in client """

    classes = models.Classes()
    classes.set_fields(dict(request.form.items()))

    db.session.add(classes)
    db.session.commit()

    return jsonify(classes=[classes.serialize() for classes in models.Classes.query.filter_by(code=classes.code)])


@classes.route('/add_student_classes/<classes_id>/<user_id>', methods=['POST'])
def add_student_classes(classes_id, user_id):
    classes = models.Classes.query.get(classes_id)
    classes.students.append(User.query.get(user_id))
    db.session.commit()
    return jsonify(classes=models.Classes.query.get(classes_id).serialize())


@classes.route('/classes_details/<classes_id>', methods=['GET'])
def classes_details(classes_id):
    return jsonify(classes=models.Classes.query.get(classes_id).serialize())

