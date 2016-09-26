from flask import  Blueprint
from functools import wraps
from flask import request, redirect, current_app, Response
from ldap3 import Server, Connection, ALL
import my_app

auth = Blueprint('auth', __name__)


def check_auth(username, password):
    try:
        server = Server(my_app.app.config['LDAP_PROVIDER_URL'], get_info=ALL)
        Connection(server, 'uid={0}, cn=users, cn=accounts, dc=demo1, dc=freeipa, dc=org'.format(username), password, auto_bind=True)
        return True
    except:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


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

@auth.route('/login', methods=['GET', 'POST'])
@ssl_required
@requires_auth
def login():
    return 'User Authenticated'


@auth.route("/")
def hello():
    return "Hello World from GitHub!"
