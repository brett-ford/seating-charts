import random
import csv

"""
Functions for altering table arrangements. 
"""


def new_tables(class_lists):
    # Creates new seating arrangement.
    print('Creating...')
    seating = {}
    prohibitions = get_prohibitions()
    for period in class_lists:
        t = number_of_tables(len(class_lists[period]))
        generate = True
        count = 0

        while generate:
            class_list = class_lists[period].copy()

            # Array to hold table groups.
            tables = []
            for i in range(t):
                tables.append([])

            # Assign students.
            while len(class_list) >= t:
                for table in tables:
                    student = random.choice(class_list)
                    class_list.remove(student)
                    table.append(student)

            # Assign leftover students.
            table_numbers = list(range(t))
            while len(class_list) > 0:
                n = random.choice(table_numbers)
                table_numbers.remove(n)
                student = random.choice(class_list)
                class_list.remove(student)
                tables[n].append(student)
            count += 1

            generate = prohibited(prohibitions, tables)

        # Extend array to 4X6.
        for table in tables:
            extend = 6 - len(table)
            for i in range(extend):
                table.append('')
        while len(tables) < 4:
                tables.append(['', '', '', '', '', ''])

        # Verify success.
        if tables:
            seating[period] = tables
            print('Period {}'.format(period))
            for i in range(t):
                print('Table {}: {}'.format(i + 1, tables[i]))
            print('Version = {}'.format(count))
        else:
            print('Failed to create tables.')

    return seating  # dictionary


def get_prohibitions():
    # Reads storage to learn the prohibitions.
    pairs = []
    with open('prohibitions.csv', 'r', newline='', encoding='utf-8-sig') as storage:
        reader = csv.reader(storage)
        for pair in reader:
            pairs.append(tuple([pair[0].strip(), pair[1].strip()]))
    return pairs  # list of tuples.


def prohibited(pairs, tables):
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


def number_of_tables(class_size):
    # Determines appropriate number of tables.
    if class_size in [1, 2, 3]:
        return 1
    if class_size in [4, 5, 6]:
        return 2
    if class_size in [7, 9]:
        return 3
    return 4
