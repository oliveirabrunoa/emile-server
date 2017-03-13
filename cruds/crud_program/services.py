from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_program.models import Program
from cruds.crud_users.models import Users
from cruds.crud_course_section_students.models import CourseSectionStudents
from cruds.crud_course_sections.models import CourseSections
from sqlalchemy import and_, or_
from cruds.crud_course_section_students_status.models import CourseSectionStudentsStatus
from sqlalchemy import func


program = Blueprint("program", __name__)


@program.route('/programs', methods=['GET'])
def programs():
    return jsonify(programs=[dict(id=program.id, name=program.name, abbreviation=program.abbreviation) for program in Program.query.all()])


@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program.serialize()), 200


@program.route('/students_program_history/<student_id>', methods=['GET'])
def students_program_history(student_id):
    student = Users.query.get(student_id)
    program = Program.query.get(student.program_id)

    students_program_history_list = []

    if not student and student.type == 1:
        return jsonify(result="invalid student id"), 404

    hours_completed, credits_completed = program_current_progress(student)
    program_details = {"hours_completed":hours_completed, "credits_completed":credits_completed ,"total_credits": program.total_credits, "total_hours": program.total_hours}
    for course in program.courses:
        _dict = {"course": course.serialize()}
        last_course_section_student = last_course_section_students(course, student)
        times = course_times(course, student)

        if not last_course_section_student:
            _dict['status'] = CourseSectionStudentsStatus.query.get(4).serialize()
            _dict['grade']= 0
        else:
            _dict['status']= CourseSectionStudentsStatus.query.get(last_course_section_student.status).serialize()
            _dict['grade']= last_course_section_student.grade
        _dict['times']= times

        students_program_history_list.append(_dict)

    return jsonify(students_program_history=[program_history for program_history in students_program_history_list], program= program_details)


def course_times(course, student):
    course_aggregation = (db.session.query(func.count(CourseSectionStudents.id)).
                                    filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                    filter(CourseSections.course_id == Courses.id).
                                    filter(Courses.program_id == Program.id).
                                    filter(Program.id == student.program_id).
                                    filter(CourseSectionStudents.user_id == student.id).
                                    filter(Courses.id == course.id).
                                    filter(or_ (CourseSectionStudents.status == 2,
                                                CourseSectionStudents.status == 3)).
                                    group_by(Courses.code,Courses.program_section).order_by(Courses.program_section).first())

    return course_aggregation[0] if course_aggregation else 0


def program_current_progress(student):
    total_hours = 0
    total_credits = 0
    program_progress = (db.session.query(Courses.hours, Courses.credits).
                                    filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                    filter(CourseSections.course_id == Courses.id).
                                    filter(Courses.program_id == Program.id).
                                    filter(Program.id == student.program_id).
                                    filter(CourseSectionStudents.user_id == student.id).
                                    filter(CourseSectionStudents.status == 2).
                                    order_by(Courses.program_section).all())

    for hours,credits in program_progress:
        total_hours = total_hours + hours
        total_credits = total_credits + credits

    return total_hours, total_credits


def last_course_section_students(course, student):
    course_section_student = (db.session.query(CourseSectionStudents).
                                    filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                    filter(CourseSections.course_id == Courses.id).
                                    filter(Courses.program_id == Program.id).
                                    filter(Program.id == student.program_id).
                                    filter(CourseSectionStudents.user_id == student.id).
                                    filter(Courses.id == course.id).
                                    order_by(CourseSections.course_section_period.desc()).first())

    return course_section_student
