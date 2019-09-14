#!/usr/bin/env python3

from authenticate import Authenticate
from seating import Seating
from storage import Storage


def main():
    """Updates seating for each selected period."""
    print('***** New Table Groups! *****')
    user_input = input("Enter period(s) or 'all':")
    credentials = Authenticate.get_credentials()  # Get Google Sheets API credentials.
    seating_chart = Seating(user_input, credentials)  # Retrieves current seating charts.
    seating_chart.update()  # New seating chart for selected periods.
    seating_chart.write_names()  # Record in Google Sheet.
    Storage(seating_chart).update_storage()  # Update seating chart in storage.
    print_seating(seating_chart.seating_chart)
    print('***** Finished *****')


def print_seating(current_seating):
    print('Verify current seating...')
    for p in current_seating:
        print('Period {}:'.format(p))
        for t in range(len(current_seating[p])):
            print('Table {}: {}'.format(t+1, current_seating[p][t]))


if __name__ == '__main__':
    main()
