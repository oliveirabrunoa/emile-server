from flask import Flask
from flask_login import LoginManager
from my_app.auth.views import auth

app = Flask(__name__)
app.config['LDAP_PROVIDER_URL'] = 'ldap://ipa.demo1.freeipa.org:389'
app.config['LDAP_PROTOCOL_VERSION'] = 3

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(auth)