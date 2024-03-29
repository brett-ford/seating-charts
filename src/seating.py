import random
import csv
import copy
import json
from datetime import datetime as dt
from googleapiclient.discovery import build
from authenticate import Authenticate
from schedule import Schedule


class Seating(Schedule):
    """
    Seating chart object for storing and updating seating arrangements.
    """
    
    app_test = False
    year = "2019_2020"

    def __init__(self, user_input):
        self.history = self.get_history()  # Past seating charts. 
        self.update_number = self.history["Updates"][-1]["Number"] + 1  # Calculate update number.
        
        self.time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')  # Time stamp for update. 

        self.periods = self.get_periods(user_input)  # Periods for which a change is requested.

        self.credentials = Authenticate.get_credentials()
        self.class_lists = self.get_class_lists()  # Current class lists.

        self.seating_chart = self.get_seating_chart()  # Current seating arrangements.
        print(self.seating_chart)

    @staticmethod
    def get_history():
        """Creates dictionary of storage contents."""
        try:
            with open('storage.json', 'r') as storage:
                history = json.load(storage)
        except Exception as e:
            print("Failed: get_history")
            print(e)
        else:
            return history  # Python dictionary

    def get_seating_chart(self):
        """Gets current seating chart from the Google Sheet."""
        seating = {}  # keys = periods, values = 2D arrays
        service = build('sheets', 'v4', credentials=self.credentials)  # Call the Sheets API
        sheet = service.spreadsheets()

        for period in self.schedules[self.year].keys():
            array = []  # Array to hold the names
            ss_range = 'Period {}!B2:G5'.format(period)  # Spreadsheet range
            try:
                result = sheet.values().get(spreadsheetId=self.seating_id, range=ss_range).execute()
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
            ss_id = self.schedules[self.year][period]['gradebook_id']  # Source spreadsheet ID

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
            tables = []  # Array to hold table groups.
            while len(tables) < t:
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
        """Writes updated seating to Google Sheet."""
        print('Writing to spreadsheet...')
        service = build('sheets', 'v4', credentials=self.credentials)  # Call Google Sheets API.

        for period in self.periods:
            if period in self.class_lists:
                seating_update = self.extend_array(copy.deepcopy(self.seating_chart[period]))
                ss_range = 'Period {}!B2:G5'.format(period)
                body = {'values': seating_update, 'majorDimension': 'rows'}
                try:
                    result = service.spreadsheets().values().update(spreadsheetId=self.seating_id,
                                                                    valueInputOption='RAW',
                                                                    range=ss_range,
                                                                    body=body).execute()
                except Exception as e:
                    print('Period {}: Failed to record names.'.format(period))
                    print(e)
                else:
                    print(result)  # Verify success

    def get_periods(self, user_input):
        """Processes user input to determine which periods need new seating arrangements."""
        active_periods = list(self.schedules[self.year].keys())
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

    def update_storage(self):
        """Writes seating update to storage.json."""
        print('Updating storage...')
        update = self.create_update()
        try:
            with open('storage.json', 'r+') as storage:
                storage_data = json.load(storage)
                storage_data["Updates"].append(update)
                storage.seek(0)
                json.dump(storage_data, storage, ensure_ascii=False, indent=4)
        except Exception as e:
            print('Update failed: {}'.format(e))
        else:
            print(update)

    def create_update(self):
        """Formats data for the storage update."""
        seating_dict = {}
        for p in self.seating_chart.keys():
            tables = {}
            for t in range(len(self.seating_chart[p])):
                tables['Table_{}'.format(t+1)] = self.seating_chart[p][t]

            seating_dict[p] = {'Course': self.schedules[self.year][p]['title'],
                               'Tables': tables}

        update = {'Number': self.update_number,
                  'Created': self.time_stamp,
                  'Periods': self.periods,
                  'App Test': self.app_test,
                  'Seating Chart': seating_dict
                  }
        return update

    def verify_seating(self):
        """Prints self.seating_chart."""
        print('Verify current seating...')
        chart = self.seating_chart
        for p in chart:
            print('Period {}:'.format(p))
            for t in range(len(chart[p])):
                print('Table {}: {}'.format(t+1, chart[p][t]))

    @staticmethod
    def get_prohibitions():
        """Reads csv to get seating restrictions."""
        prohibitions = []
        with open('prohibitions.csv', 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
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
    def number_of_tables(class_size):
        """Determines appropriate number of tables for a given class size."""
        if class_size in [1, 2, 3]:
            return 1
        if class_size in [4, 5, 6]:
            return 2
        if class_size in [7, 9]:
            return 3
        return 4

    @staticmethod
    def extend_array(array):
        """Extends array to 4X6."""
        for row in array:
            while len(row) < 6:
                row.append('')
        while len(array) < 4:
            array.append(['', '', '', '', '', ''])
        return array


if __name__=="__main__":
    s = Seating("23")
    print(s.history["Updates"][-1])
    print(type(s.history))
    print(s.update_number)
