from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_from_aws():
    return "Hello from aws!"
