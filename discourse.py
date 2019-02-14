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


def days_ago(number_of_days):
    from datetime import datetime, timedelta
    return (datetime.today() - timedelta(days=number_of_days)).date().isoformat()


def generate_discourse_report_url(base_url, report_name, start_date, end_date, username, api_token):
    """Return the Discourse API endpoint url with *base_url* and *timestamp* attached"""
    return "{}/admin/reports/{}.json?end_date={}&start_date={}&api_key={}&api_username={}".format(base_url, report_name, end_date, start_date, api_token, username)


def fetch_report_from_discourse(report_name, headers, base_url, start_date, end_date, username, token):
    print("Fetching {} from {} to {}...".format(
        report_name, start_date, end_date))
    url = generate_discourse_report_url(
        base_url, report_name, start_date, end_date, username, token)
    response = requests.get(url)
    report_data = json.loads(response.text)['report']

    with open('data/discourse/discourse_{}.json'.format(report_name), 'w') as f:
        f.write(response.text)

    with open('data/discourse/discourse_{}.csv'.format(report_name), 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(
            headers)
        for item in report_data['data']:
            csvwriter.writerow([item['x'], item['y']])


def main():

    end_date = days_ago(1)
    start_date = days_ago(31)

    fetch_report_from_discourse('posts', ['date', 'count'], DISCOURSE_URL, start_date,
                                end_date, DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)

    fetch_report_from_discourse('accepted_solutions', ['date', 'count'], DISCOURSE_URL, start_date,
                                end_date, DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)

    fetch_report_from_discourse('time_to_first_response', ['date', 'hours_to_first_response'], DISCOURSE_URL, start_date,
                                end_date, DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)


if __name__ == '__main__':
    sys.exit(main())
