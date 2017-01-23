from flask import jsonify, Blueprint, request
from . import models
from backend import db
from cruds.crud_course_sections.models import CourseSections


users = Blueprint("user", __name__)


@users.route('/users', methods=['GET'])
def get_users():
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.Users.query.all()])


@users.route('/students', methods=['GET'])
def get_students():
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.Users.query.filter_by(type=1)])


@users.route('/teachers', methods=['GET'])
def get_teachers():
    return jsonify(users=[dict(id=user.id, username=user.username) for user in models.Users.query.filter_by(type=2)])


@users.route('/add_user', methods=['POST'])
def add_users():
    #This method it was implemented considering that all fields are required in client
    user = models.Users()
    user.set_fields(dict(request.form.items()))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(username=user.username)])


@users.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])


@users.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    user = models.Users.query.get(user_id)

    if user:
        user.set_fields(dict(request.form.items()))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@users.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = models.Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in models.Users.query.all()])
    return jsonify(result='invalid user id')


@users.route('/teachers_course_sections/<teacher_id>', methods=['GET'])
def teachers_course_sections(teacher_id):
    teacher = models.Users.query.filter_by(id=teacher_id, type=2).first()
    if teacher:
        teachers_course_sections = CourseSections.query.filter_by(teacher_id=teacher_id)
        return jsonify(teachers_course_sections=[course_section.serialize() for course_section in teachers_course_sections])
    return jsonify(result='invalid teacher id')


@users.route('/students_course_sections/<student_id>', methods=['GET'])
def students_course_sections(student_id):
    student = models.Users.query.filter_by(id=student_id, type=1).first()

    if student:
        return jsonify(students_course_sections=[course_sections_students.course_section.serialize() for course_sections_students in student.course_sections])
    return jsonify(result='invalid student id')
