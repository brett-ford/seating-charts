import csv
import json
from datetime import datetime as dt


class Storage:
    def __init__(self, schedule, periods, seating_chart):
        self.time_stamp = dt.today().strftime('%Y-%m-%d %H:%M:%S')
        self.periods = periods
        self.app_test = False
        self.schedule = schedule
        self.seating_chart = seating_chart

    def log_update(self):
        print(self.seating_chart.seating_chart)
        seating_dict = {}
        for p in self.seating_chart.seating_chart.keys():
            tables = {}
            for t in range(4):
                tables['table_{}'.format(t+1)] = self.seating_chart.seating_chart[p][t]

            seating_dict[p] = {'course': self.schedule[p]['Title'],
                               'tables': tables}
        log_update = {'time_stamp': self.time_stamp,
                      'periods_updated': self.periods,
                      'app_test': self.app_test,
                      'seating_chart': seating_dict
                      }
        return log_update

        # store = json.dumps(seating_information, indent=4)
