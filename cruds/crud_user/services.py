from flask import jsonify, Blueprint, request
from . import models
from backend import db


user = Blueprint("user", __name__)


@user.route('/users', methods=['GET'])
def get_users():
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.User.query.all()])


@user.route('/add_user', methods=['POST'])
def add_users():
    """ This method it was implemented considering that all fields are required in client """

    user = models.User()
    user.set_fields(dict(request.form.items()))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(username=user.username)])


@user.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])


@user.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    """ This method allows to update from kwargs """

    user = models.User.query.get(user_id)

    if user:
        user.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.User.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@user.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = models.User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in models.User.query.all()])
    return jsonify(result='invalid user id')


@user.route('/classes_teacher/<teacher_id>', methods=['GET'])
def classes_teacher(teacher_id):
    teacher = models.User.query.filter_by(id=teacher_id, type="teacher").first()
    if teacher:
        return jsonify(classes_teacher=[classes.serialize() for classes in teacher._classes.all()])
    return jsonify(result='invalid teacher id')