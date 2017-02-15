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


program = Blueprint("program", __name__)

from sqlalchemy import func
@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program.serialize()), 200

#Need to refactory
@program.route('/students_program_history/<student_id>', methods=['GET'])
def students_program_history(student_id):
    student = Users.query.get(student_id)
    program = Program.query.get(student.program_id)

    students_program_history_list = []

    if not student and student.type == 1:
        return jsonify(result="invalid student id"), 404

    program_details = {"credits_completed":0, "hours_completed":0 , "total_credits": program.total_credits, "total_hours": program.total_hours}
    for course in program.courses:
        _dict = {"course": course.serialize()}
        course_times = (db.session.query(func.count(CourseSectionStudents.id),CourseSectionStudents, Courses).
                                        filter(CourseSectionStudents.course_section_id == CourseSections.id).
                                        filter(CourseSections.course_id == Courses.id).
                                        filter(Courses.program_id == Program.id).
                                        filter(Program.id == student.program_id).
                                        filter(CourseSectionStudents.user_id == student_id).
                                        filter(Courses.id == course.id).
                                        filter(or_ (CourseSectionStudents.status == 2,
                                                    CourseSectionStudents.status == 3,
                                                    CourseSectionStudents.status == 1)).
                                        group_by(Courses.code).order_by(CourseSectionStudents.id.desc()).first())

        if not course_times:
            continue

        if course_times[1].status == 2:
            program_details.update({'credits_completed': program_details['credits_completed'] + course_times[2].credits})
            program_details.update({'hours_completed': program_details['hours_completed'] + course_times[2].hours})

        _dict['status']= CourseSectionStudentsStatus.query.get(course_times[1].status).serialize()
        _dict['grade']= course_times[1].grade
        _dict['times']= course_times[0]

        if course_times[1].status == 1:
            _dict['times']= course_times[0]-1

        students_program_history_list.append(_dict)

    return jsonify(students_program_history=[program_history for program_history in students_program_history_list], program= program_details)
