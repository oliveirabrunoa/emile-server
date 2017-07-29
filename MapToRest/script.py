import importlib
from MapToRest.db_config import Base, db_session, engine, meta
from MapToRest.render_template import render_to_template
import json


class LoadModelClasses(object):

    def __init__(self, loader_models):
        self.LOADER_MODEL_CLASSES = loader_models


    def import_modules(self):
        model_list = []
        for model in self.LOADER_MODEL_CLASSES:
            module_name, class_name = model.rsplit('.', maxsplit=1)
            m = importlib.import_module(module_name)
            cls = getattr(m, class_name)
            model_list.append(cls)

        return model_list

    def table_names(self):
        for table in meta.sorted_tables:
            print(table)

    def generate_base_file(self):
        models_list = self.import_modules()
        data_to_render = []

        for att_classs in models_list:
            data = {"model_name": att_classs.__modelname__, "table_name": att_classs.__tablename__}
            attributes = []
            for attribute in att_classs.__attributes__:
                attributes.append(attribute)
            data['attributes']= attributes
            data_to_render.append(data)
        render_to_template("MapToRest/model.json", "configuration_file.html",data)
        return True


    def generate_new_models(self):
        data_config = self.open_config_file()
        list_models=[]
        for model in data_config:
            dict_model = {
                "model_name": model.get('model_name')+'Base',
                "table_name": model.get('table_name'),
                "attributes": [model.get('attributes')]
                }
            list_models.append(dict_model)
            render_to_template("MapToRest/new_model.py", "template_model.py",dict_model)
        

    def open_config_file(self):
        with open('MapToRest/model.json') as data_file:
            data = json.load(data_file)
        return data
