from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_program.models import Program
from cruds.crud_users.models import Users
from cruds.crud_course_section_students.models import CourseSectionStudents
from cruds.crud_course_sections.models import CourseSections


program = Blueprint("program", __name__)

from sqlalchemy import func
@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program.serialize()), 200

#2. passa o id de um aluno e retorna a grade curricular, mas já dizendo quais disicplinas ele cursou.
@program.route('/students_program_history/<student_id>', methods=['GET'])
def students_program_history(student_id):
    student = Users.query.get(student_id)
    students_program_history = []

    if not student and student.type == 1:
        return jsonify(result="invalid student id"), 404

    program = Program.query.get(student.program_id)
    courses = program.courses

    for course in courses:
        _dict = {"course": course.serialize()}
        a = (db.session.query(func.count(CourseSectionStudents.id)).filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                        filter(CourseSections.course_id == Courses.id).
                                        filter(Courses.program_id == Program.id).
                                        filter(Program.id == student.program_id).
                                        filter(CourseSectionStudents.user_id == student_id).
                                        filter(Courses.id == course.id).group_by(Courses.id).all())
        for b in a:
            print(b)








    # a = (db.session.query(Courses).filter(CourseSectionStudents.course_section_id == CourseSections.id).
    #                                 filter(CourseSections.course_id == Courses.id).
    #                                 filter(Courses.program_id == Program.id).
    #                                 filter(Program.id == student.program_id).all())
    # for b in a:
        # print(b.serialize())
    # for course in courses:
    #     _dict = {"course": course.serialize()}
    #     a =(db.session.query(CourseSectionStudents).join(CourseSectionStudents).
    #                                     filter(CourseSections.course_id == Courses.id).
    #                                     filter(Courses.program_id == Program.id).
    #                                     filter(Program.id == student.program_id).all())
    #
    # for b in a:
    #     print(a.serialize())










    return "ok"
