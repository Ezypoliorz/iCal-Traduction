from flask import Flask, Response, request
import requests
from icalendar import Calendar
import re

app = Flask(__name__)

PRONOTE_URL = "https://0141274j.index-education.net/pronote/ical/mesinformations.ics?icalsecurise=7477663A2115621F4A21B48A2908E73279E304A87A2150D76D5CBBD85B973F28462FB0173283D8E11EB56A9C149A39F4&version=2025.2.6&param=900A75DF9ED8C62E212781A9E4DCC937"

@app.route('/calendrier')
def proxy_ical():
    response = requests.get(PRONOTE_URL)
    cal = Calendar.from_ical(response.content)

    for event in cal.walk('VEVENT'):
        summary = str(event.get('summary'))
        new_summary = summary.split(' - ')[0]
        event['summary'] = new_summary

        description = str(event.get('description'))
        description = re.sub(r"(Groupe|Parties de classe) : .*", "", description)
        event['description'] = description.strip()

    return Response(cal.to_ical(), mimetype='text/calendar')