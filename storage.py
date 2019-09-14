import json


class Storage:
    """Stores seating chart updates in json format."""

    test = False

    def __init__(self, seating_chart):
        self.seating_chart = seating_chart

    def update_storage(self):
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
            for t in range(len(self.seating_chart.seating_chart[p])):
                tables['Table_{}'.format(t+1)] = self.seating_chart.seating_chart[p][t]

            seating_dict[p] = {'Course': self.seating_chart.mb_2019_2020[p]['title'],
                               'Tables': tables}

        update = {'Created': self.seating_chart.time_stamp,
                  'Periods': self.seating_chart.periods,
                  'App Test': self.test,
                  'Seating Chart': seating_dict
                  }
        return update
