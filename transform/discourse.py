"""Script for transforming report data from Discourse"""
import csv
import datetime
import json
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def days_ago(number_of_days):
    return (datetime.today() - timedelta(days=number_of_days)).date().isoformat()


def write_data_as_csv(start_date, end_date, report_name, data, headers):
    # prep the raw data
    raw_data = data['data']
    intermediate_data = dict()
    for each_record in raw_data:
        intermediate_data[each_record['x']] = each_record['y']

    df = pd.DataFrame(intermediate_data, index=['date'])
    df = df.T
    missing_data = df.to_dict()
    missing_data = missing_data['date']

    # generate the time series
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_array = \
        (start + timedelta(days=x)
         for x in range(0, (end-start).days))

    # populate the clean data with the time series
    full_data = {}
    for date_object in date_array:
        full_data[date_object.strftime("%Y-%m-%d")] = 0

    # add the raw date over the time series
    for date in missing_data:
        full_data[date] = missing_data[date]

    try:
        with open('data/discourse/discourse_{}.csv'.format(report_name), 'x') as output:
            csvwriter = csv.writer(output)
            csvwriter.writerow(
                headers)

            # write the csv
            for item in full_data:
                csvwriter.writerow([item, full_data[item]])
    except FileExistsError:
        print('Skipping the saving of {}, file already exists'.format(report_name))


def main():

    report_names = ['posts', 'accepted_solutions',
                    'time_to_first_response', 'daily_engaged_users', 'dau_by_mau']

    end_date = days_ago(1)
    start_date = days_ago(31)
    today = datetime.today().strftime("%Y-%m-%d")

    for report_name in report_names:
        print("Transforming {} from {} to {} from JSON to CSV...".format(
            report_name, start_date, end_date))
        with open('data/discourse/discourse_{}_{}_{}_{}.json'.format(
                report_name, 'range', start_date, end_date), 'r') as input:
            report_data = json.loads(input.read())['report']

            write_data_as_csv(start_date, end_date, '{}_{}_{}_{}'.format(
                report_name, 'range', start_date, end_date), report_data, ['date', 'count'])

        print("Transforming daily {} for {} from JSON to CSV...".format(
            report_name, today))
        with open('data/discourse/discourse_{}_{}_{}.json'.format(
                report_name, 'daily', today), 'r') as input:
            report_data = json.loads(input.read())['report']

            write_data_as_csv(today, today, '{}_{}_{}'.format(
                report_name, 'daily', today), report_data, ['date', 'count'])


if __name__ == '__main__':
    sys.exit(main())
