from flask import  Blueprint
from flask import request
from auth.app import login_manager
from flask_login import logout_user, login_required, login_user
from auth.models import User


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not User.try_login(username, password):
        return "Invalid credentials!"
    user = User(username, password)
    login_user(user)
    return "Login successfullly"


@auth.route("/",  methods=['GET', 'POST'])
@login_required
def hello():
    return "Hello World from GitHub!"


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return "logout successfullly"

@login_manager.user_loader
def load_user(user):
    return User.get(user)