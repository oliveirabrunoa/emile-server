from flask import Blueprint, jsonify
from . import models
from backend import db
from cruds.crud_user.models import User
from cruds.crud_classes.models import Classes
import datetime
from sqlalchemy import and_


lesson = Blueprint("lesson", __name__)


@lesson.route('/lesson_in_progress/<teacher_id>', methods=['GET'])
def lesson_in_progress(teacher_id):
    lessons = (db.session.query(models.Lesson).filter(User.id == Classes.teacher_id).
               filter(Classes.id == models.Lesson.classes_id).
               filter(User.id == teacher_id).
               filter(and_(datetime.datetime.now() >= models.Lesson.lesson_start_date,
                           datetime.datetime.now() <= models.Lesson.lesson_finish_date)).all())
    return jsonify(lesson=[lesson.serialize() for lesson in lessons])