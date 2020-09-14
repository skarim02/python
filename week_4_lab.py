#!/usr/bin/env python3

import csv
import datetime
import requests
import pprint
from collections import defaultdict

FILE_URL = "https://storage.googleapis.com/gwg-hol-assets/gic215/employees-with-date.csv"
def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()
    return datetime.datetime(year, month, day)

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

##intializations
data = get_file_lines(FILE_URL)
reader = csv.reader(data[1:])
new_lines = [line for line in reader]
new_lines = sorted(new_lines, key=lambda x: x[3])
d = defaultdict(list)
for each in new_lines:
    d[datetime.datetime.strptime(each[3], '%Y-%m-%d')].append("{} {}".format(each[0], each[1]))

def get_same_or_newer(start_date):
    for each_line in d:
        if each_line < start_date:
            continue
        if each_line < datetime.datetime.today():
            print("Started on {}: {}".format(each_line.strftime("%b %d, %Y"), d[each_line]))
        start_date = start_date + datetime.timedelta(days=1)

def main():

    start_date = get_start_date()
    get_same_or_newer(start_date)

if __name__ == "__main__":
    main()


