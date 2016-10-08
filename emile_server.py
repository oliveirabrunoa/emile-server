from flask import Flask, request
import json
import settings
import importlib

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    module_name, class_name = settings.AUTHENTICATION_BACKEND.rsplit('.', maxsplit=1)
    m = importlib.import_module(module_name)
    cls = getattr(m, class_name)            

    email = request.form.get('email')
    password = request.form.get('password')

    return cls().authenticate(email, password)

if __name__=='__main__':
    app.run(debug=True)
