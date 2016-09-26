import ldap3
from flask import  url_for, Blueprint, g
from flask_login import current_user, login_user, \
    logout_user, login_required
from my_app import login_manager, db
from my_app.auth.models import User
from functools import wraps
from flask import request, redirect, current_app
import json

auth = Blueprint('auth', __name__)

def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

    return decorated_view

@ssl_required
@auth.route('/login', methods=['GET', 'POST'])
def login_ssl():

    if request.method =='POST':
        user = request.form.get('user')
        password = request.form.get('password')
        try:
            User.try_login(user, password)
        except:
            return 'credenciais invalidas!'

        return 'Login efetuado'

    else:
        return 'Método não permitido'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))