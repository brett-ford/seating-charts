from datetime import datetime as dt
import csv


def record(periods):
    # Records a time stamp and which period was updated.
    print('Recording...')

    time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')
    log_update = [time_stamp] + list(periods)

    try:
        with open('log.csv', 'a') as log:
            writer = csv.writer(log)
            writer.writerow(log_update)
    except Exception as e:
        print('Failed to update: {}'.format(log_update))
        print(e)
    else:
        print('Log Update: {}'.format(log_update))
