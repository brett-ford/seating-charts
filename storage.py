import json
from datetime import datetime as dt


class Storage:
    """Stores seating chart updates in json format."""

    app_test = True

    def __init__(self, schedule, periods, seating_chart):
        self.time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')
        self.periods = periods
        self.schedule = schedule
        self.seating_chart = seating_chart

    def create_update(self):
        seating_dict = {}
        for p in self.seating_chart.seating_chart.keys():
            tables = {}
            for t in range(4):
                tables['table_{}'.format(t+1)] = self.seating_chart.seating_chart[p][t]

            seating_dict[p] = {'course': self.schedule[p]['Title'],
                               'tables': tables}
        log_update = {'created': self.time_stamp,
                      'periods': self.periods,
                      'app_test': self.app_test,
                      'seating_chart': seating_dict
                      }
        return log_update

    def store(self):
        print('Updating storage...')
        update = self.create_update()
        try:
            with open('storage.json', 'r+') as storage:
                storage_data = json.load(storage)
                storage_data["Updates"].append(update)
                storage.seek(0)
                json.dump(storage_data, storage, ensure_ascii=False, indent=4)
        except:
            pass
        else:
            print(update)

    @staticmethod
    def reduce_array(array):
        for i in range(4):
            for j in range(6):
                if array[i][j] == '':
                    del array[i][j]
