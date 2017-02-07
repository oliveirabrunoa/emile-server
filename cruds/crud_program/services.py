from flask import Blueprint, jsonify, request
from . import models
from backend import db
from cruds.crud_courses.models import Courses
from cruds.crud_program.models import Program


program = Blueprint("program", __name__)


@program.route('/programs_courses/<program_id>', methods=['GET'])
def programs_courses(program_id):
    program = Program.query.get(program_id)
    if not program:
        return jsonify(result="invalid program id"), 404
    return jsonify(program=program.serialize()), 200
