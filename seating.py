import random
import csv
import copy
from datetime import datetime as dt

from googleapiclient.discovery import build

from schedule import Schedule


class Seating(Schedule):
    """Seating chart object for storing and updating seating arrangements."""

    def __init__(self, user_input, credentials):
        self.time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')
        self.periods = self.get_periods(user_input)  # Periods for which a change is requested.
        self.credentials = credentials
        self.seating_chart = self.get_seating_chart()
        self.class_lists = self.get_class_lists()

    def get_seating_chart(self):
        """Gets current seating chart."""

        seating = {}  # keys = periods, values = 2D arrays
        ss_id = self.seating_id
        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API
        sheet = service.spreadsheets()

        for period in self.mb_2019_2020.keys():
            array = []  # Array to hold the names
            ss_range = 'Period {}!B2:G4'.format(period)  # Spreadsheet range
            try:
                result = sheet.values().get(spreadsheetId=ss_id, range=ss_range).execute()
                values = result.get('values', [])
            except Exception as e:
                print('Period {}: Failed to read.'.format(period))
                print(e)
            else:
                if not values:
                    print('Period {}: No data found.'.format(period))
                else:
                    for row in values:
                        array.append(row)
                    seating[period] = array
        return seating  # keys = periods, values = 2D arrays

    def get_class_lists(self):
        """Gets class list for each requested period."""

        print('Getting class lists...')
        students = {}  # key = periods, values = list of names
        ss_range = 'Summary!B3:H40'  # Spreadsheet range for source sheet.
        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API
        sheet = service.spreadsheets()

        for period in self.periods:
            class_list = []  # Array to hold the names
            ss_id = self.mb_2019_2020[period]['source_id']  # Source spreadsheet ID

            try:
                result = sheet.values().get(spreadsheetId=ss_id, range=ss_range).execute()
                values = result.get('values', [])
            except Exception as e:
                print('Period {}: Failed to read.'.format(period))
                print(e)
            else:
                if not values:
                    print('Period {}: No data found.'.format(period))  # Unlikely error.
                else:
                    for row in values:
                        if int(row[-1]) == period:
                            class_list.append(row[0].strip() + ' ' + row[1][0].strip() + '.')
                    students[period] = class_list
                    print('Period {}: {}'.format(period, students[period]))  # Success.
        return students  # keys = periods, values = list of names

    def update(self):
        """Updates seating for the requested periods."""

        print('Updating seating chart...')
        for period in self.periods:
            if period in self.class_lists:
                new_seating, version = self.new_tables(period)
                self.seating_chart[period] = new_seating

                # Verify success:
                if new_seating:
                    print('Period {}'.format(period))
                    for i in range(len(new_seating)):
                        print('Table {}: {}'.format(i + 1, new_seating[i]))
                    print('Version = {}'.format(version))
                else:
                    print('Period {}: Failed to update seating.'.format(period))

    def new_tables(self, period):
        """Creates new table groups."""

        class_list = self.class_lists[period]
        prohibitions = self.get_prohibitions()
        t = self.number_of_tables(len(class_list))
        count = 0

        while True:
            students = class_list.copy()

            # Array to hold table groups.
            tables = []
            for i in range(t):
                tables.append([])

            # Assign students.
            while len(students) >= t:
                for table in tables:
                    student = random.choice(students)
                    students.remove(student)
                    table.append(student)

            # Assign leftover students.
            table_numbers = list(range(t))
            while len(students) > 0:
                n = random.choice(table_numbers)
                table_numbers.remove(n)
                student = random.choice(students)
                students.remove(student)
                tables[n].append(student)

            count += 1

            if not self.prohibited(tables, prohibitions):
                return tables, count  # 2D array, number of builds.

    def write_names(self):
        """writes updated seating charts to Google Sheet."""

        print('Writing to spreadsheet...')
        ss_id = self.seating_id
        service = build('sheets', 'v4', credentials=self.credentials)  # Call Google Sheets API.

        for period in self.periods:
            if period in self.class_lists:
                seating_update = self.extend_array(copy.deepcopy(self.seating_chart[period]))
                ss_range = 'Period {}!B2:G5'.format(period)
                body = {'values': seating_update, 'majorDimension': 'rows'}
                try:
                    result = service.spreadsheets().values().update(spreadsheetId=ss_id,
                                                                    valueInputOption='RAW',
                                                                    range=ss_range,
                                                                    body=body).execute()
                except Exception as e:
                    print('Period {}: Failed to record names.'.format(period))
                    print(e)
                else:
                    print(result)  # Verify success

    def get_periods(self, user_input):
        active_periods = list(self.mb_2019_2020.keys())
        if user_input == 'all':
            periods = active_periods.copy()
            print('New Seats: {}'.format(periods))
            return periods
        choices = list(user_input)
        periods = []
        for choice in choices:
            try:
                p = int(choice)
            except ValueError:
                pass
            else:
                if p in active_periods:
                    periods.append(p)
        if periods:
            print('New Seats: {}'.format(periods))
            return periods
        else:
            print('Invalid input.')
            print('***** Finished *****')
            exit()

    @staticmethod
    def get_prohibitions():
        """Reads .csv to get seating restrictions."""
        prohibitions = []
        with open('prohibitions.csv', 'r', newline='', encoding='utf-8-sig') as storage:
            reader = csv.reader(storage)
            for pair in reader:
                prohibitions.append(tuple([pair[0].strip(), pair[1].strip()]))
        return prohibitions  # list of tuples.

    @staticmethod
    def prohibited(groups, prohibitions):
        """Determines if the seating chart violates any prohibited pairs."""
        for group in groups:
            for pair in prohibitions:
                intersection = set(group).intersection(set(pair))
                size = len(intersection)
                if size == 2:
                    return True
        return False

    @staticmethod
    def number_of_tables(s):
        """Determines appropriate number of tables for a given class size."""
        if s in [1, 2, 3]:
            return 1
        if s in [4, 5, 6]:
            return 2
        if s in [7, 9]:
            return 3
        return 4

    @staticmethod
    def extend_array(array):
        """Extends 2D array to 4X6."""
        for row in array:
            extend = 6 - len(row)
            for i in range(extend):
                row.append('')
        while len(array) < 4:
            array.append(['', '', '', '', '', ''])
        return array
