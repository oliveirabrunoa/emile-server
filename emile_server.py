from flask import Flask
import settings
import backend
from pathlib import Path
from cruds.crud_aluno import views


def create_app(backend_path=''):
    app = Flask("emile")
    app.config['SQLALCHEMY_DATABASE_URI'] = backend_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    backend.db.init_app(app)
    my_file = Path(settings.DB_PATH)

    if not my_file.is_file():
        with app.app_context():
            backend.db.create_all()
    return app


app = create_app(settings.BACKEND_PATH)


if __name__ == '__main__':
    app.register_blueprint(views.user)
    app.run(debug=True)
