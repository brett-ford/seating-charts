#!/usr/bin/env python3

from seating import Seating
from storage import Storage


def main():
    """Updates seating for each selected period."""
    print('***** New Table Groups! *****')
    user_input = input("Enter period(s) or 'all':")

    seating_chart = Seating(user_input)  # Retrieves current seating.
    seating_chart.update()  # New seating for selected periods.
    seating_chart.write_names()  # Record in Google Sheet.

    Storage(seating_chart).update_storage()  # Append new seating to storage.

    seating_chart.verify_seating()
    print('***** Finished *****')


if __name__ == '__main__':
    main()
