#!/usr/bin/env python3

from authenticate import Authenticate
from seating import Seating
from storage import Storage

"""Assigns students to new table groups."""


def main():
    """Main"""
    print('***** New Table Groups! *****')
    user_input = input("Enter period(s) or 'all':")
    credentials = Authenticate.get_credentials()  # Authenticate to Google Sheets API.
    seating_chart = Seating(user_input, credentials)  # Retrieves current seating charts.
    seating_chart.update()  # New seating chart for selected periods.
    seating_chart.write_names()  # Record in Google Sheet.
    Storage(seating_chart).update_storage()  # Update seating chart in storage.
    print(seating_chart.seating_chart)
    print('***** Finished *****')


if __name__ == '__main__':
    main()
