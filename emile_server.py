from flask import Flask, request
import json
import settings

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    parts = settings.AUTHENTICATION_BACKEND.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            

    email = request.form.get('email')
    password = request.form.get('password')

    return m().authenticate(email, password)

if __name__=='__main__':
    app.run(debug=True)
