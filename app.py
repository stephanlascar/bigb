from flask import Flask
from flask_pydantic import validate

from models import AddLogEventModel

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/events/logs/add')
@validate()
def add_log_event(body: AddLogEventModel):
    print(body.url)
    return "", 201
