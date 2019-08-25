import random
import csv

from googleapiclient.discovery import build


"""For creating and storing new seating arrangements."""


class Seating:
    """Seating chart object for current seats."""
    def __init__(self, schedule, periods, credentials, class_lists):
        self.schedule = schedule
        self.periods = periods
        self.credentials = credentials
        self.class_lists = class_lists
        self.seating_chart = self.get_seating()

    def get_seating(self):
        """Gets current seating chart."""
        seating = {}  # keys = periods, values = 2D arrays
        ss_id = '1M8jlCnl7OOpg0Dh4BIYZqyC977qHZhwEUh9WOJU7HOA'

        # Call the Sheets API
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet = service.spreadsheets()

        for period in self.schedule.keys():
            chart = []  # Array to hold the names
            ss_range = 'Period {}!B2:G4'.format(period)  # Spreadsheet range
            try:
                result = sheet.values().get(spreadsheetId=ss_id, range=ss_range).execute()
                values = result.get('values', [])
            except Exception as e:
                print('Failed to read: period {}.'.format(period))
                print(e)
            else:
                if not values:
                    print('No data found: period {}.'.format(period))
                else:
                    for table in values:
                        chart.append(table)
                    seating[period] = self.extend_array(chart)
        return seating

    def update(self):
        """Updates seating for the requested periods."""
        print('Updating seats...')
        for period in self.periods:
            self.seating_chart[period] = self.new_tables(period)

    def new_tables(self, period):
        """Creates new table groups."""
        class_list = self.class_lists.names[period]
        prohibitions = self.get_prohibitions()
        t = self.number_of_tables(len(class_list))
        prohibited = True
        count = 0

        while prohibited:
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
            prohibited = self.prohibited(tables, prohibitions)

        # Verify success.
        if tables:
            print('Period {}'.format(period))
            for i in range(t):
                print('Table {}: {}'.format(i + 1, tables[i]))
            print('Version = {}'.format(count))
        else:
            print('Failed to create tables.')

        return self.extend_array(tables)  # 2D array extended to 4X6

    def write_names(self):
        """writes updated seating charts to Google Sheet."""
        print('Writing to spreadsheet...')

        ss_id = '1M8jlCnl7OOpg0Dh4BIYZqyC977qHZhwEUh9WOJU7HOA'
        service = build('sheets', 'v4', credentials=self.credentials)

        for period in self.periods:
            if self.seating_chart[period]:
                ss_range = 'Period {}!B2:G5'.format(period)
                body = {'values': self.seating_chart[period], 'majorDimension': 'rows'}
                try:
                    result = service.spreadsheets().values().update(spreadsheetId=ss_id,
                                                                    valueInputOption='RAW',
                                                                    range=ss_range,
                                                                    body=body).execute()
                except Exception as e:
                    print('Failed to update: period {}'.format(period))
                    print(e)
                else:
                    # Verify success
                    print(result)
            else:
                print('Empty: period {}'.format(period))

    @staticmethod
    def get_prohibitions():
        # Reads storage to learn the prohibitions.
        pairs = []
        with open('prohibitions.csv', 'r', newline='', encoding='utf-8-sig') as storage:
            reader = csv.reader(storage)
            for pair in reader:
                pairs.append(tuple([pair[0].strip(), pair[1].strip()]))
        return pairs  # list of tuples.

    @staticmethod
    def prohibited(tables, pairs):
        # Determines if the seating chart violates an prohibited pairs.
        # Inputs: pairs, a list of tuples, and tables, a list of lists.
        # Output: boolean -- True if prohibited pair, false otherwise.
        for table in tables:
            for pair in pairs:
                intersection = set(table).intersection(set(pair))
                size = len(intersection)
                if size == 2:
                    return True
        return False

    @staticmethod
    def number_of_tables(class_size):
        # Determines appropriate number of tables.
        if class_size in [1, 2, 3]:
            return 1
        if class_size in [4, 5, 6]:
            return 2
        if class_size in [7, 9]:
            return 3
        return 4

    @staticmethod
    def extend_array(tables):
        """Extend 2D array to 4X6."""
        for table in tables:
            extend = 6 - len(table)
            for i in range(extend):
                table.append('')
        while len(tables) < 4:
            tables.append(['', '', '', '', '', ''])
        return tables
