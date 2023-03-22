from flask import Flask

app = Flask(__name__)
host = "localhost"
port = 8080




if __name__ == '__main__':
    app.run(host=host, port=port)