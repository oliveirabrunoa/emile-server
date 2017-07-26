import importlib
from MapToRest.db_config import Base, db_session, engine, meta
from MapToRest.render_template import render_to_template
import json

LOADER_MODEL_CLASSES = ['cruds.crud_course_type.models.CourseType']

class LoadModelClasses:

    def import_modules(self):
        model_list = []
        for model in LOADER_MODEL_CLASSES:
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
        render_to_template("model.json", "configuration_file.html",data)


    def generate_new_models(self):
        data_config = self.open_config_file()
        list_models=[]
        for data in data_config:
            a = {
                "model_name": data.get('model_name')+'Base',
                "table_name": data.get('table_name'),
                "attributes": [data.get('attributes')]
                }
            list_models.append(a)
        #Montar o model que herda de base, de acordo com as configurações do dicionário retornado.
        #falta aplicar a todos os modelos!!!!
        print(list_models)
        render_to_template("new_model.py", "template_model.py",a)





    def open_config_file(self):
        with open('model.json') as data_file:
            data = json.load(data_file)
        return data




if __name__ == '__main__':
    l = LoadModelClasses()
    l.generate_new_models()
    #l.generate_new_models()



#ACESSAR A LISTA DE MODELS
#FAZER IMPORT E LEITURA DE ATRIBUTOS
#LER SCHEMA DO BANCO
