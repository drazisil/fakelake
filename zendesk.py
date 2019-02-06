"""Script for fetching ticket comments from Zendesk"""
import csv
from dotenv import load_dotenv
import json
import os
import requests
import sys
load_dotenv()

ZENDESK_URL = os.getenv("ZENDESK_URL")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")


def generateZendeskUrl(base_url, timestamp):
    """Return the Zendesk API endpoint url with *base_url* and *timestamp* attached"""
    return "{}/api/v2/incremental/ticket_events.json?start_time={}&include=comment_events".format(base_url, timestamp)


def main():
    from datetime import datetime, timedelta

    d = datetime.today() - timedelta(days=7)
    url = generateZendeskUrl(ZENDESK_URL, int(d.timestamp()))
    user = "{}/token".format(ZENDESK_EMAIL)
    response = requests.get(url, auth=(
        user, ZENDESK_API_TOKEN))
    ticket_comments = json.loads(response.text)

    with open('output.csv', 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(
            ['id', 'type', 'author_id', 'html_body', 'public?', "created_at", 'event_type'])
        first_record_event = ticket_comments.get(
            'ticket_events')[0].get('child_events')[0]
        print(first_record_event)
        for event in ticket_comments.get('ticket_events'):
            # print("id {}, updated by updater_id {} has {} child_events".format(
                # event.get('id'), event.get('updater_id'), len(event.get('child_events'))))
            if len(event.get('child_events')) > 1:
                for child_event in event.get('child_events'):
                    csvwriter.writerow([child_event.get('id'), child_event.get('type'), child_event.get(
                        'author_id'), child_event.get('html_body'), child_event.get('public'), child_event.get('created_at'), child_event.get('event_type')])


if __name__ == '__main__':
    sys.exit(main())
