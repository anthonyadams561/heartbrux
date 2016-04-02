#!/usr/bin/env python
import argparse
import re
import datetime
import pandas


def process_data(data_file):
    regex_date = re.compile('Year,(?P<year>\d{4}),Month,(?P<month>\d+),Day,(?P<day>\d+),'
                            'Hour,(?P<hour>\d+),Minute,(?P<minute>\d+),Second,(?P<second>\d+)')

    regex_heartrate = re.compile ("\A(?P<seconds>\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),"
                                  "(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),"
                                  "(?P<heartrate>\d*\.*\d*)")
    start_datetime = None

    in_data_section = False

    heartrate_column_name = "hr_heartrate"

    for line in data_file:
        # Look for the start date and time
        if start_datetime is None:
            match = regex_date.match(line)
            if match:
                year = int(match.group("year"))
                month = int(match.group("month"))
                day = int(match.group("day"))
                hour = int(match.group("hour"))
                minute = int(match.group("minute"))
                second = int(match.group("second"))
                start_datetime = datetime.datetime(year, month, day, hour, minute, second)
                print start_datetime

        if heartrate_column_name in line:
            in_data_section = True

        # Does this line contain heartrate data?
        if in_data_section:
            match = regex_heartrate.match(line)
            if match:
                seconds = int(match.group("seconds"))
                heartrate = int(match.group("heartrate"))


def main():
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('data_file', type=argparse.FileType('r'), help='The data file to process')
    args = parser.parse_args()
    process_data(args.data_file)


if __name__ == "__main__":
    main()
