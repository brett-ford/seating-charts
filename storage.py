import json
from datetime import datetime as dt

from schedule import Schedule


class Storage:
    """Stores seating chart updates in json format."""

    app_test = True

    def __init__(self, periods, seating_chart):
        self.time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')
        self.periods = periods
        self.seating_chart = seating_chart

    def store(self):
        """Writes seating update to storage.json."""
        print('Updating storage...')
        update = self.create_update()
        try:
            with open('storage.json', 'r+') as storage:
                storage_data = json.load(storage)
                storage_data["Updates"].append(update)
                storage.seek(0)
                json.dump(storage_data, storage, ensure_ascii=False, indent=4)
        except Exception as e:
            print('Update failed: {}'.format(e))
        else:
            print(update)

    def create_update(self):
        """Formats data for the storage update."""
        seating_dict = {}
        for p in self.seating_chart.seating_chart.keys():
            tables = {}
            for t in range(4):
                tables['table_{}'.format(t+1)] = self.seating_chart.seating_chart[p][t]

            seating_dict[p] = {'Course': self.schedule[p]['Title'],
                               'Tables': tables}

        update = {'Created': self.time_stamp,
                  'Periods': self.periods,
                  'App Test': self.app_test,
                  'Seating Chart': seating_dict
                  }
        return update
