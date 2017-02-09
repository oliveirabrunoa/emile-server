from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_program.models import Program
from cruds.crud_users.models import Users
from cruds.crud_course_section_students.models import CourseSectionStudents
from cruds.crud_course_sections.models import CourseSections
from sqlalchemy import and_, or_


program = Blueprint("program", __name__)

from sqlalchemy import func
@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program.serialize()), 200


@program.route('/students_program_history/<student_id>', methods=['GET'])
def students_program_history(student_id):
    student = Users.query.get(student_id)
    students_program_history_list = []

    if not student and student.type == 1:
        return jsonify(result="invalid student id"), 404

    program = Program.query.get(student.program_id)
    courses = program.courses

    for course in courses:
        _dict = {"course": course.serialize()}
        course_times = (db.session.query(func.count(CourseSectionStudents.id)).
                                        filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                        filter(CourseSections.course_id == Courses.id).
                                        filter(Courses.program_id == Program.id).
                                        filter(Program.id == student.program_id).
                                        filter(CourseSectionStudents.user_id == student_id).
                                        filter(Courses.id == course.id).
                                        filter(or_ (CourseSectionStudents.status == 'Aprovado',
                                                    CourseSectionStudents.status == 'Reprovado')).
                                        group_by(Courses.code).first())
        last_status = (db.session.query(CourseSectionStudents.status).
                                        filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                        filter(CourseSections.course_id == Courses.id).
                                        filter(Courses.program_id == Program.id).
                                        filter(Program.id == student.program_id).
                                        filter(CourseSectionStudents.user_id == student_id).
                                        filter(Courses.id == course.id).
                                        filter(or_ (CourseSectionStudents.status == 'Aprovado',
                                                    CourseSectionStudents.status == 'Reprovado',
                                                    CourseSectionStudents.status == 'Cursando')).
                                        order_by(CourseSectionStudents.id.desc()).first())
        if not course_times:
            course_times = (0,)
        if not last_status:
            last_status = ('Não cursada',)

        _dict['times']= course_times[0]
        _dict['status']= last_status[0]

        students_program_history_list.append(_dict)

    return jsonify(students_program_history=[program_history for program_history in students_program_history_list])
