"""Script for transforming report data from Discourse"""
import csv
import json
import sys
import numpy as np
import pandas as pd


def days_ago(number_of_days):
    from datetime import datetime, timedelta
    return (datetime.today() - timedelta(days=number_of_days)).date().isoformat()


def write_data_as_csv(start_date, end_date, report_name, data, headers):
    with open('data/discourse/discourse_{}.csv'.format(report_name), 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(
            headers)

        # dr = pd.date_range(start_date, end_date)
        # df = pd.Series(data['data'])

        raw_data = data['data']
        print(raw_data)
        intermediate_data = dict()
        for each_record in raw_data:
            intermediate_data[each_record['x']] = each_record['y']

        df = pd.DataFrame(intermediate_data, index=['date'])
        df = df.T

        print(df)

        for item in data['data']:
            csvwriter.writerow([item['x'], item['y']])


def main():

    report_names = ['posts', 'accepted_solutions', 'time_to_first_response']
    report_names = ['accepted_solutions']

    end_date = days_ago(1)
    start_date = days_ago(31)

    for report_name in report_names:
        with open('data/discourse/discourse_{}_{}_{}.json'.format(
                report_name, start_date, end_date), 'r') as input:
            report_data = json.loads(input.read())['report']

            write_data_as_csv(start_date, end_date, '{}_{}_{}'.format(
                report_name, start_date, end_date), report_data, ['date', 'count'])


if __name__ == '__main__':
    sys.exit(main())
