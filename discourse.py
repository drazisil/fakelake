"""Script for fetching report data from Discourse"""
import csv
from dotenv import load_dotenv
import json
import os
import requests
import sys
load_dotenv()

DISCOURSE_URL = os.getenv("DISCOURSE_URL")
DISCOURSE_USERNAME = os.getenv("DISCOURSE_USERNAME")
DISCOURSE_API_TOKEN = os.getenv("DISCOURSE_API_TOKEN")


def generateDiscourseUrl(base_url, report_name, start_date, end_date, username, api_token):
    """Return the Discourse API endpoint url with *base_url* and *timestamp* attached"""
    return "{}/admin/reports/{}.json?end_date={}&start_date={}&api_key={}&api_username={}".format(base_url, report_name, end_date, start_date, api_token, username)


def main():
    from datetime import datetime, timedelta

    report_name = 'accepted_solutions'
    end_date = (datetime.today() - timedelta(days=1)).date().isoformat()
    start_date = (datetime.today() - timedelta(days=31)).date().isoformat()
    print("Fetching {} from {} to {}...".format(
        report_name, start_date, end_date))
    url = generateDiscourseUrl(
        DISCOURSE_URL, report_name, start_date, end_date, DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)
    response = requests.get(url)
    report_data = json.loads(response.text)['report']

    with open('data/discourse/discourse_accepted_solutions.csv', 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(
            ['date', 'count'])
        for item in report_data['data']:
            csvwriter.writerow([item['x'], item['y']])


if __name__ == '__main__':
    sys.exit(main())
