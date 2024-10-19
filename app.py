import datetime
import os
from typing import Optional

import requests
from bs4 import BeautifulSoup
import psycopg
import pytz
from flask import Flask, request
from flask_cors import CORS
from flask_pydantic import validate
from flask_executor import Executor

from models import AddLogEventModel

DATABASE_URI = os.environ.get("DATABASE_URL")
DATABASE_URI = "postgresql://bigb_user:HSWUnTa1t1SITdWyN8l5xr3qytesGzTE@dpg-cs9rvhjqf0us739m3ldg-a.frankfurt-postgres.render.com/bigb"
API_KEY = os.environ.get("API_KEY", "You will never guess!")

app = Flask(__name__)
CORS(app)
executor = Executor(app)


def get_log_event_local_datetime(date: str, timezone: str) -> datetime:
    parsed_date = datetime.datetime.fromisoformat(date[:-1])
    utc_timezone = pytz.timezone('UTC')
    aware_date = parsed_date.replace(tzinfo=utc_timezone)
    user_timezone = pytz.timezone(timezone) if timezone in pytz.all_timezones else utc_timezone

    return aware_date.astimezone(user_timezone).replace(tzinfo=None)


def get_website_description(url: str) -> Optional[str]:
    try:
        response = requests.get(url if url.startswith('http') else f'http://{url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        description_tag = soup.find('meta', attrs={'name': 'description'})

        if not description_tag:
            return None

        return description_tag.get('content')
    except:
        return None


def save_log_event(body: AddLogEventModel):
    with psycopg.connect(DATABASE_URI) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO event_log (device_id, local_datetime, title, url, description) VALUES (%s, %s, %s, %s, %s)",
                (
                    body.id,
                    get_log_event_local_datetime(body.date, body.timezone),
                    body.title,
                    body.url,
                    get_website_description(body.url)
                ))

            conn.commit()


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

    executor.submit(save_log_event, body)
    return "", 201
