import importlib
import json
from emile_server import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import csv
from cruds.crud_users.models import Users
from cruds.crud_course_sections.models import CourseSections
from cruds.crud_course_section_students_status.models import CourseSectionStudentsStatus
import random


# an Engine, which the Session will use for connection
# resources
some_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


# create a configured "Session" class
Session = sessionmaker(bind=some_engine)


# create a Session
session = Session()


def load_data():
    user_id = session.query(Users).get(1)
    program_history = []
    fields =[]

    with open('eliakim_history.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            program_history.append(row)

        for item in program_history:
            print(item[1])
            course_section = course_section_id=session.query(CourseSections).filter_by(course_section_period=item[0], code=item[1]).first()
            if not course_section:


            _temp = dict(course_section_id=session.query(CourseSections).filter_by(course_section_period=item[0], code=item[1]).first().id,
                         user_id=user_id.id,
                         status=session.query(CourseSectionStudentsStatus).filter_by(description=item[2]).first().id,
                         grade=item[3])

            fields.append(dict(model='cruds.crud_course_section_students.models.CourseSectionStudents', fields= _temp))

    data_to_json = json.dumps(fields, indent=2,sort_keys=False)
    file_path = './initial_data/'+'{0}_CourseSectionStudents_{1}.{2}'.format(random.randrange(12, 100),user_id.username,'json')

    commit(data_to_json)
    generate_file(file_path,data_to_json)




def commit(data_to_json):
    data = json.loads(data_to_json)
    model_relative_path = 'cruds.crud_course_section_students.models.CourseSectionStudents'
    for item in data:
        module_path, model_name = str(model_relative_path).rsplit('.', maxsplit=1)
        model = getattr(importlib.import_module(module_path), model_name)

        kwargs = item['fields']
        obj = model()
        obj.set_fields(kwargs)
        session.add(obj)
        session.commit()


def generate_file(file_path,data_to_json):
    new_file= open(file_path, 'w')
    new_file.write(data_to_json)
    new_file.close()


if __name__=='__main__':
    load_data()
