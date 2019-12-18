#!/usr/local/bin/python3.7
"""Previous interpretor: /usr/bin/env python3"""

from seating import Seating


def main():
    """Updates seating for each selected period."""
    print('******* New Table Groups! *******')
    user_input = input("Enter period(s) or 'all':")

    seating_chart = Seating(user_input)  # Retrieves current seating.
    seating_chart.update()  # New seating for selected periods.
    seating_chart.write_names()  # Record in Google Sheet.
    seating_chart.update_storage()  # Add new seating to storage.
    seating_chart.verify_seating()  # Print out current state of seating object.
    print('******* Finished *******')


if __name__ == '__main__':
    main()
