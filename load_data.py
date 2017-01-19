import importlib
import json
from emile_server import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# an Engine, which the Session will use for connection
# resources
some_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


# create a configured "Session" class
Session = sessionmaker(bind=some_engine)


# create a Session
session = Session()


def load_data():
    with open('./initial_data/data.json') as data_file:
        data = json.load(data_file)

        for item in data:
            model_relative_path = item['model']
            module_path, model_name = str(model_relative_path).rsplit('.', maxsplit=1)
            model = getattr(importlib.import_module(module_path), model_name)

            kwargs = item['fields']
            obj = model()
            obj.set_fields(kwargs)
            session.add(obj)
            session.commit()


if __name__=='__main__':
    load_data()
