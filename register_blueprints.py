import os
import importlib
import string


def register_blueprints(app):
    for module in os.listdir(os.getcwd() + '/blueprints/'):
        if 'blueprints' in module:
            module_name = module.replace('.py', '')
            class_name = string.capwords(module_name.replace('_', ' ')).replace(' ', '')
            cls = getattr(importlib.import_module('blueprints.{0}'.format(module_name)), class_name)
            blueprints =  cls().blueprints()

            for blueprint in blueprints:
                app.register_blueprint(blueprint)
