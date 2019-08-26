from googleapiclient.discovery import build

from schedule import Schedule

"""This class stores the data needed to update the seating charts."""


class StudentData(Schedule):
    """Retrieves and stores the data needed to create new seating charts."""

    def __init__(self, schedule, periods, credentials):
        self.schedule = schedule
        self.periods = periods
        self.credentials = credentials
        self.names = self.get_names()

    def get_names(self):
        """Gets student names for all requested periods."""
        print('Reading...')
        names = {}
        for period in self.periods:
            names[period] = self.get_list(period)
        return names  # keys = periods, values = list of names

    def get_list(self, period):
        """Reads one period's class list."""
        class_list = []  # Array to hold the names
        ss_id = self.schedule[period]['Sheet_ID']  # Spreadsheet ID
        ss_range = 'Summary!B3:H30'  # Spreadsheet range

        # Call the Sheets API
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet = service.spreadsheets()

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
                for student in values:
                    if int(student[-1]) == period:
                        class_list.append(student[0].strip() + ' ' + student[1][0].strip() + '.')
            # Verify success
            if class_list:
                print('Period {}: {}'.format(period, class_list))
            else:
                print('Failed to get names: period {}'.format(period))

        return class_list  # 1D array
