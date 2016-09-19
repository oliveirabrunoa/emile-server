from flask import Flask
emile_server = Flask(__name__)

@emile_server.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    emile_server.run()
