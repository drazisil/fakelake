"""Script for fetching report data from Discourse"""
import csv
from dotenv import load_dotenv
import json
import os
import requests
import sys
from datetime import datetime, timedelta

print(os.getcwd())

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")

DISCOURSE_URL = os.getenv("DISCOURSE_URL")
DISCOURSE_USERNAME = os.getenv("DISCOURSE_USERNAME")
DISCOURSE_API_TOKEN = os.getenv("DISCOURSE_API_TOKEN")


def days_ago(number_of_days):
    return (datetime.today() - timedelta(days=number_of_days)).date().isoformat()


def generate_discourse_report_url(base_url, report_name, start_date, end_date, username, api_token):
    """Return the Discourse API endpoint url with *base_url* and *timestamp* attached"""
    return "{}/admin/reports/{}.json?end_date={}&start_date={}&api_key={}&api_username={}".format(base_url, report_name, end_date, start_date, api_token, username)


def write_data_as_json(report_name, data):
    with open('data/discourse/discourse_{}.json'.format(report_name), 'w') as f:
        f.write(data)


def fetch_range_report_from_discourse(report_name, base_url, start_date, end_date, username, token):
    print("Fetching {} from {} to {}...".format(
        report_name, start_date, end_date))
    url = generate_discourse_report_url(
        base_url, report_name, start_date, end_date, username, token)
    response = requests.get(url)

    write_data_as_json('{}_{}_{}_{}'.format(
        report_name, 'range', start_date, end_date), response.text)


def fetch_daily_report_from_discourse(report_name, base_url, username, token):
    today = datetime.today().strftime("%Y-%m-%d")
    print("Fetching daily report {} for {}...".format(
        report_name, today))
    url = generate_discourse_report_url(
        base_url, report_name, today, today, username, token)
    response = requests.get(url)

    write_data_as_json('{}_{}_{}'.format(
        report_name, 'daily', today), response.text)


def main():

    end_date = days_ago(1)
    start_date = days_ago(31)

    reports = ['posts', 'accepted_solutions',
               'time_to_first_response', 'daily_engaged_users', 'dau_by_mau']

    for report in reports:

        fetch_range_report_from_discourse(report, DISCOURSE_URL, start_date,
                                          end_date, DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)

        fetch_daily_report_from_discourse(report, DISCOURSE_URL,
                                          DISCOURSE_USERNAME, DISCOURSE_API_TOKEN)


if __name__ == '__main__':
    sys.exit(main())
