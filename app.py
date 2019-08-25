#!/usr/bin/env python3

from authenticate import get_credentials
from schedule import Schedule
from student_data import Names
from seating import Seating
from storage import Storage

""""Assigns students to new table groups."""


def main():
    """Main"""
    print('***** New Table Groups! *****')
    user_input = input("Enter period(s) or 'all':")
    schedule = Schedule().mb_2019_2020  # Retrieve current schedule.
    periods = process_input(user_input, schedule)  # Input the class period.
    credentials = get_credentials()  # Authenticate
    class_lists = Names(schedule, periods, credentials)  # Get students' names.
    seating_chart = Seating(schedule, periods, credentials, class_lists)  # Retrieves current seating charts.
    seating_chart.update()  # New seating chart for selected periods.
    seating_chart.write_names()  # Record in Google Sheet.

    print(Storage(schedule, periods, seating_chart).log_update())
    # storage.record(new_tables.keys())  # Store new seating chart.
    print('***** Finished *****')


def process_input(user_input, schedule):
    active_periods = list(schedule.keys())
    if user_input == 'all':
        periods = active_periods.copy()
        print(periods)
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
        print(periods)
        return periods
    else:
        print('Invalid input.')
        print('***** Finished *****')
        exit()


if __name__ == '__main__':
    main()
