from flask import  Blueprint
from functools import wraps
from flask import request, redirect, current_app
from ldap3 import Server, Connection, ALL
import my_app
from flask_login import login_required
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
@login_required
@auth.route('/login', methods=['GET', 'POST'])
def login_ssl():

    if request.method =='POST':
        user = request.form.get('user')
        password = request.form.get('password')
        try:
            server = Server(my_app.app.config['LDAP_PROVIDER_URL'], get_info=ALL)
            Connection(server,'uid={0}, cn=users, cn=accounts, dc=demo1, dc=freeipa, dc=org'.format(user),
                              password, auto_bind=True)
        except:
            return 'Invalid credentials!'

        return 'Login successfully!'

    else:
        return 'Method Not Allowed'


@auth.route("/")
def hello():
    return "Hello World from GitHub!"
