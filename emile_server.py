from flask import Flask
from flask import request
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE
import json

app = Flask(__name__)
app.secret_key = 'dsajifjwq98f9qw8f98qw9fqwfkjqwofjw9qf89qw'

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        server = Server(host='10.1.0.4', get_info=ALL)
        conn = Connection(server, user=email, password=password, auto_bind=True)
        conn.search(search_base='DC=intranet, DC=cefetba, DC=br',search_filter='(sAMAccountName={0})'.format(str(email).split('@')[0]),search_scope=SUBTREE, attributes=ALL_ATTRIBUTES)
        entry = conn.entries[0]
        data = {'firstName': str(entry.givenName), 'lastName': str(entry.sn)}
        return json.dumps(data)
    except:
        return json.dumps({"result":"Invalid credentials!"})

if __name__=='__main__':
  app.run(debug=True)