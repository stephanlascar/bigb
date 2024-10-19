import os

import psycopg
from flask import Flask
from flask_pydantic import validate

from models import AddLogEventModel

DATABASE_URI = os.environ.get("DATABASE_URL")

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/events/logs/add')
@validate()
def add_log_event(body: AddLogEventModel):
    with psycopg.connect(DATABASE_URI) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO event_log (device_id, local_datetime, title, url) VALUES (%s, %s, %s, %s)",
                (body.id, body.date, body.title, body.url))

            conn.commit()

    return "", 201
