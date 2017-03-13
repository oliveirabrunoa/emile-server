from flask import jsonify, Blueprint, request, url_for, send_from_directory
from . import models
from backend import db
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_course_section_students.models import CourseSectionStudents
from cruds.crud_program.models import Program
from cruds.crud_courses.models import Courses
from cruds.crud_institution.models import Institution
import os
from werkzeug.utils import secure_filename
import settings


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


@users.route('/add_student', methods=['POST'])
def add_student():
    data = dict(request.get_json())

    try:
        user = models. Users(email=data['email'], password=data['password'], program_id=data['program_id'], type=1)
        db.session.add(user)
        db.session.commit()

        course_sections_ids = data['course_sections']

        for course_sections_id in course_sections_ids:
            course_section = CourseSections.query.get(course_sections_id)
            student = models.Users.query.filter_by(email=data['email']).first()

            course_section_students = CourseSectionStudents(course_section_id=course_sections_id, user_id=student.id, grade=0, status=1)
            course_section_students.course_section = course_section
            student.course_sections.append(course_section_students)

        db.session.commit()
        return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(email=user.email)]), 200
    except Exception as e:
        return jsonify(result='invalid request'), 400


@users.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])


# @users.route('/update_user/<user_id>', methods=['POST'])
# def update_user(user_id):
#     user = models.Users.query.get(user_id)
#
#     if user:
#         user.set_fields(dict(request.get_json()))
#         db.session.commit()
#         return jsonify(user=[user.serialize() for user in models.Users.query.filter_by(id=user_id)])
#     return jsonify(result='invalid user id')


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
        teachers_course_sections = (db.session.query(CourseSections).
                                    filter(Institution.id==Program.institution_id).
                                    filter(Program.id==Courses.program_id).
                                    filter(Courses.id==CourseSections.course_id).
                                    filter(CourseSections.teacher_id==teacher_id).
                                    filter(CourseSections.course_section_period==Institution.current_program_section).all())

        return jsonify(teachers_course_sections=[course_section.serialize() for course_section in teachers_course_sections])
    return jsonify(result='invalid teacher id')


@users.route('/students_course_sections/<student_id>', methods=['GET'])
def students_course_sections(student_id):
    """ It returns just course_sections in progress """
    student = models.Users.query.filter_by(id=student_id, type=1).first()

    if not student:
        return jsonify(result='invalid student id')

    students_course_sections_list = student.course_sections
    current_course_sections = []

    for course_section_student in students_course_sections_list:
        if course_section_student.status == 1:
            current_course_sections.append(course_section_student)

    return jsonify(students_course_sections=[course_sections_students.course_section.serialize() for course_sections_students in current_course_sections])



@users.route('/token_register/<user_id>', methods=['POST'])
def token_register(user_id):
    post_message = request.get_json()['post_message']
    user = models.Users.query.get(user_id)

    if user:
        user.push_notification_token = post_message['push_notification_token']
        db.session.commit()
        return jsonify(user= user.serialize()), 200

    return jsonify(result = 'invalid user id'), 404


@users.route('/update_user_image/<user_id>', methods=['POST'])
def update_user_image(user_id):
    user = models.Users.query.get(user_id)
    if not user:
        return jsonify(result='invalid user id'), 404
    if 'image_file' not in request.files:
        return jsonify(result='No file part'), 404

    file = request.files['image_file']

    if file.filename == '':
        return jsonify(result='No selected file'), 400
    if not file or not allowed_file(file.filename):
        return jsonify(result='File with invalid format'), 400

    filename = secure_filename(file.filename)
    if not user.save_image(file):
        jsonify(user=models.Users.query.get(user_id).serialize()), 400

    db.session.commit()
    return jsonify(user=models.Users.query.get(user_id).serialize()), 200

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS or 'asset.JPG' in filename)
