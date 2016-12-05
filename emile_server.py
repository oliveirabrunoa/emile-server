from flask import Flask
import backend
import os
from cruds.crud_user import services as user_services
from cruds.crud_subject import services as subject_services
from cruds.crud_classes import services as classes_services


def create_app():
    app = Flask("emile")

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    backend.db.init_app(app)
    return app


app = create_app()
app.register_blueprint(user_services.user)
app.register_blueprint(subject_services.subject)
app.register_blueprint(classes_services.classes)

if __name__ == '__main__':
    app.run()
