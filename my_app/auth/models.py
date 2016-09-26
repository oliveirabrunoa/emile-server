from ldap3 import Server, Connection, ALL
from my_app import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username

    @staticmethod
    def try_login(username, password):
        server = Server(app.config['LDAP_PROVIDER_URL'], get_info=ALL)
        conn = Connection(server, 'uid={0}, cn=users, cn=accounts, dc=demo1, dc=freeipa, dc=org'.format(username), password, auto_bind=True)


    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)