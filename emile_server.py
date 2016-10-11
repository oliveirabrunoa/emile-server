from flask import Flask, request
import settings
import importlib
from models import db, User
from flask import jsonify


def create_app(backend_path=''):
    app = Flask("emile")
    app.config['SQLALCHEMY_DATABASE_URI'] = backend_path
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app(settings.BACKEND_PATH)


@app.route('/login', methods=['POST'])
def login():
    module_name, class_name = settings.AUTHENTICATION_BACKEND.rsplit('.', maxsplit=1)
    m = importlib.import_module(module_name)
    cls = getattr(m, class_name)            

    email = request.form.get('email')
    password = request.form.get('password')

    return cls().authenticate(email, password)


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users=[user.serialize() for user in User.query.all()])


@app.route('/add_user', methods=['POST'])
def add_users():
    username = request.form.get('username')
    email = request.form.get('email')

    if username and email:
        user = User(username, email)
        db.session.add(user)
        db.session.commit()
        return jsonify(user=[user.serialize() for user in User.query.filter_by(username=username)])

if __name__ == '__main__':
    app.run(debug=True)
