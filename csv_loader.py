import importlib
from emile_server import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import csv
import csv_loader_classes


# an Engine, which the Session will use for connection
# resources
some_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


# create a configured "Session" class
Session = sessionmaker(bind=some_engine)


# create a Session
session = Session()



class CSVLoader:

    def load_data(self):
        files = sorted(os.listdir(os.getcwd() + '/initial_data/'))

        for crud_csv in files:
            if crud_csv.rsplit('.', maxsplit=1)[1] == 'csv':
                with open('./initial_data/'+ crud_csv) as data_file:
                    reader = csv.reader(data_file)
                    for row in reader:
                        obj = self.create_object(row)
                        session.add(obj)
                        session.commit()

    def import_relative_path(self, model_relative_path):
        module_path, model_name = str(model_relative_path).rsplit('.', maxsplit=1)
        return getattr(importlib.import_module(module_path), model_name)

    def create_object(self, row):
        raise NotImplementedError("Subclasses should implement this!")

if __name__=='__main__':
    csv_loader = CSVLoader()

    for relative_path in csv_loader_classes.CSV_LOADER_CLASSES:
        cls = csv_loader.import_relative_path(relative_path)
        cls().load_data()