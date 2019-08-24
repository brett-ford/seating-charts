from googleapiclient.discovery import build

"""Functions that work with the Google Sheets API."""


def get_names(schedule, period, credentials):
    # Gets student names for all requested sections.
    print('Reading...')
    names = {}
    if period == 8:
        for p in schedule:
            names[p] = get_list(schedule, p, credentials)
    else:
        names[period] = get_list(schedule, period, credentials)
    return names  # dictionary[period] = list of names


def get_list(schedule, period, credentials):
    # Reads one class list.

    class_list = []  # Array to hold the names
    ss_id = schedule[period]['Sheet_ID']  # Spreadsheet ID
    ss_range = 'Summary!B3:H30'  # Spreadsheet range

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=credentials)
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
            print('Failed to get names.')

    return class_list  # 1D array


def write_names(credentials, seating):
    # Write to file.
    print('Writing...')

    spreadsheet_id = '1M8jlCnl7OOpg0Dh4BIYZqyC977qHZhwEUh9WOJU7HOA'
    service = build('sheets', 'v4', credentials=credentials)

    for period in seating:
        if seating[period]:
            spreadsheet_range = 'Period {}!B2:G5'.format(period)
            body = {'values': seating[period], 'majorDimension': 'rows'}
            try:
                result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                                valueInputOption='RAW',
                                                                range=spreadsheet_range,
                                                                body=body).execute()
            except Exception as e:
                print('Failed to update: period {}'.format(period))
                print(e)
            else:
                # Verify success
                print(result)
        else:
            print('Empty: period {}'.format(period))
