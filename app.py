#!/usr/bin/env python3

import authenticate
from schedule import Schedule
import sheets
import tables
import storage

""""Assigns students to new table groups."""


def main():
    """Main"""
    print('***** New Table Groups! *****')
    schedule = Schedule().mb_2019_2020  # Retrieve current schedule.
    period = process_input(schedule, input('Period:'))  # Input the class period.
    credentials = authenticate.get_credentials()  # Authenticate
    class_lists = sheets.get_names(schedule, period, credentials)  # Get students' names.
    new_tables = tables.new_tables(class_lists)  # Randomly assign names to tables.
    sheets.write_names(credentials, new_tables)  # Record assignments in a spreadsheet.
    storage.record(new_tables.keys())
    print('***** Finished *****')


def process_input(schedule, period):
    valid_entries = ['1', '2', '3', '4', '5', '6', '7', 'all']
    active_periods = list(schedule.keys())

    if period not in valid_entries:
        print('Invalid entry: {}'.format(period))
        print('***** Finished *****')
        exit()
    else:
        if period == 'all':
            return 8
        else:
            period = int(period)
            if period in active_periods:
                return period
            else:
                print('{} is a free period.'.format(period))
                print('***** Finished *****')
                exit()


if __name__ == '__main__':
    main()
