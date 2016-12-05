from flask import Blueprint, jsonify, request
from . import models
from backend import db


subject = Blueprint("subject", __name__)

@subject.route('/subjects', methods=['GET'])
def get_subjects():
    return jsonify(subjects=[dict(id=subject.id, code=subject.code) for subject in models.Subject.query.all()])


@subject.route('/add_subject', methods=['POST'])
def add_subject():
    subject = models.Subject()
    subject.set_fields(dict(request.form.items()))

    db.session.add(subject)
    db.session.commit()

    return jsonify(subject=[subject.serialize() for subject in models.Subject.query.filter_by(code=subject.code)])


@subject.route('/subject_details/<subject_id>', methods=['GET'])
def subject_details(subject_id):
    return jsonify(subject=[subject.serialize() for subject in models.Subject.query.filter_by(id=subject_id)])