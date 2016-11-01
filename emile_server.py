
from flask import Flask, request
import settings
import importlib
from models import db, User
from flask import jsonify
import datetime

app = Flask("emile")
app.config['SQLALCHEMY_DATABASE_URI'] = settings.BACKEND_PATH
db.init_app(app)


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
    return jsonify(users=[dict(id=user.id, username=user.username) for user in User.query.all()])


@app.route('/add_user', methods=['POST'])
def add_users():
    """ This method it was implemented considering that all fields are required in client """

    user = User()

    for attr in request.form.keys():
        if attr == "birth_date":
            setattr(user, attr, datetime.datetime.strptime(request.form.get('birth_date'), "%m-%d-%Y").date())
        else:
            setattr(user, attr, request.form.get(attr))

    db.session.add(user)
    db.session.commit()

    return jsonify(user=[user.serialize() for user in User.query.filter_by(username=user.username)])


@app.route('/user_details/<user_id>', methods=['GET'])
def user_details(user_id):
    return jsonify(user=[user.serialize() for user in User.query.filter_by(id=user_id)])


@app.route('/update_user/<user_id>', methods=['POST'])
def update_user(user_id):
    """ This method allows to update from kwargs """

    user = User.query.get(user_id)

    if user:
        for attr in request.form.keys():
            if attr == "birth_date":
                setattr(user, attr,
                        datetime.datetime.strptime(request.form.get('birth_date'), "%m-%d-%Y").date())
            else:
                setattr(user, attr, request.form.get(attr))
        db.session.commit()
        return jsonify(user=[user.serialize() for user in User.query.filter_by(id=user_id)])
    return jsonify(result='invalid user id')


@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(users=[user.serialize() for user in User.query.all()])
    return jsonify(result='invalid user id')


if __name__ == '__main__':
    app.run(debug=True)
