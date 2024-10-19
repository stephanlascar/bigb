import datetime
import os

import psycopg
import pytz
from flask import Flask, request
from flask_cors import CORS
from flask_pydantic import validate

from models import AddLogEventModel

DATABASE_URI = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("API_KEY", "You will never guess!")

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/events/logs/add', methods=['POST'])
@validate()
def add_log_event(body: AddLogEventModel):
    headers = request.headers
    api_key = headers.get("X-Api-Key")
    if api_key != API_KEY:
        return "", 401

    parsed_date = datetime.datetime.fromisoformat(body.date[:-1])
    utc_timezone = pytz.timezone('UTC')
    aware_date = parsed_date.replace(tzinfo=utc_timezone)

    local_datetime = aware_date.astimezone(pytz.timezone(body.timezone)).replace(tzinfo=None)

    with psycopg.connect(DATABASE_URI) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO event_log (device_id, local_datetime, title, url) VALUES (%s, %s, %s, %s)",
                (body.id, local_datetime, body.title, body.url))

            conn.commit()

    return "", 201
