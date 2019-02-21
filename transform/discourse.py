"""Script for transforming report data from Discourse"""
import csv
import datetime
import json
import sys
import numpy as np
import pandas as pd


def days_ago(number_of_days):
    from datetime import datetime, timedelta
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
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_array = \
        (start + datetime.timedelta(days=x)
         for x in range(0, (end-start).days))

    # populate the clean data with the time series
    full_data = {}
    for date_object in date_array:
        full_data[date_object.strftime("%Y-%m-%d")] = 0

    # add the raw date over the time series
    for date in missing_data:
        full_data[date] = missing_data[date]

    with open('data/discourse/discourse_{}.csv'.format(report_name), 'w') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerow(
            headers)

        # write the csv
        for item in full_data:
            csvwriter.writerow([item, full_data[item]])


def main():

    report_names = ['posts', 'accepted_solutions', 'time_to_first_response']

    end_date = days_ago(1)
    start_date = days_ago(31)

    for report_name in report_names:
        print("Trasforming {} from {} to {} from JSON to CSV...".format(
            report_name, start_date, end_date))
        with open('data/discourse/discourse_{}_{}_{}.json'.format(
                report_name, start_date, end_date), 'r') as input:
            report_data = json.loads(input.read())['report']

            write_data_as_csv(start_date, end_date, '{}_{}_{}'.format(
                report_name, start_date, end_date), report_data, ['date', 'count'])


if __name__ == '__main__':
    sys.exit(main())
