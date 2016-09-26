from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os.path


app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = 'ldap://ipa.demo1.freeipa.org:389'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from my_app.auth.views import auth
app.register_blueprint(auth)

db.create_all()