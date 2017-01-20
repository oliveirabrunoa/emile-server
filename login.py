import importlib
from flask import request, Blueprint
import settings


login = Blueprint("login", __name__)


@login.route('/login', methods=['POST'])
def login_service():
    module_name, class_name = settings.AUTHENTICATION_BACKEND.rsplit('.', maxsplit=1)
    m = importlib.import_module(module_name)
    cls = getattr(m, class_name)

    email = request.form.get('email')
    password = request.form.get('password')

    return cls().authenticate(email, password)
