import datetime
import re
from pandas import Series


# Extracts heart rate and time data from a Wahoo Fitness log file and returns a Pandas Series
def parse(data_file):
    regex_date_time = re.compile('Year,(?P<year>\d{4}),Month,(?P<month>\d+),Day,(?P<day>\d+),'
                                 'Hour,(?P<hour>\d+),Minute,(?P<minute>\d+),Second,(?P<second>\d+)')

    regex_heart_rate = re.compile("\A(?P<seconds>\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),"
                                  "(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),"
                                  "(?P<heartrate>\d*\.*\d*)")
    start_datetime = None
    in_data_section = False

    heart_rate_column_name = "hr_heartrate"

    time_data = []
    heart_rate_data = []

    for line in data_file:
        # Look for the start date and time
        if start_datetime is None:
            match = regex_date_time.match(line)
            if match:
                year = int(match.group("year"))
                month = int(match.group("month"))
                day = int(match.group("day"))
                hour = int(match.group("hour"))
                minute = int(match.group("minute"))
                second = int(match.group("second"))
                start_datetime = datetime.datetime(year, month, day, hour, minute, second)

        if heart_rate_column_name in line:
            in_data_section = True

        # Does this line contain heart rate data?
        if in_data_section:
            match = regex_heart_rate.match(line)
            if match:
                seconds = int(match.group("seconds"))
                heart_rate = int(match.group("heartrate"))
                heart_rate_data.append(heart_rate)
                time_data.append(start_datetime + datetime.timedelta(seconds=seconds))

    return Series(heart_rate_data, index=time_data)

