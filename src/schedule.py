class Schedule:
    """
    This class stores schedules, info related to schedules, and other information.
    """

    schedules = {'2019_2020': {2: {'title': 'Linear Algebra',
                                   'code': 'LA',
                                   'gradebook_id': '1hLkmhn--f4e6u024lrm0eSY1fGsKFD73vNpmMo2Dedc',
                                   'folder_id': '1yas-XAxlEeDFzS7m93MpX3-nEhosaFf8'},
                               3: {'title': 'AP Calculus BC',
                                   'code': 'BC',
                                   'gradebook_id': '1oIzl4sNT7P1WNXft_xKnlypG-8N8SsB-9TkDNqF0VzE',
                                   'folder_id': '1PiYtw3FV0bdLsOWPja8U_Ylp8rCo_jy6'},
                               5: {'title': 'Honors Precalculus',
                                   'code': 'HPC',
                                   'gradebook_id': '1Pz570BbfsgP-FrxALqvi3vR_IedIvqceS1hM6ixBSOw',
                                   'folder_id': '1na7goDAbFfiUIQn42IRiiXBtjLBk2zkW'},
                               6: {'title': 'Honors Precalculus',
                                   'code': 'HPC',
                                   'gradebook_id': '1Pz570BbfsgP-FrxALqvi3vR_IedIvqceS1hM6ixBSOw',
                                   'folder_id': '1na7goDAbFfiUIQn42IRiiXBtjLBk2zkW'},
                               }
                 }

    seating_id = '1M8jlCnl7OOpg0Dh4BIYZqyC977qHZhwEUh9WOJU7HOA'  # Record seating charts here. 

    # TODO: write code that reads csv files from myMB to set up schedule for the new year and store in a json file.
    # @staticmethod
    # def get_schedule():
    #     schedule = {}
    #     for period in range(1, 8):
    #         try:
    #             with open('period_{}.csv'.format(period), 'r') as file:
    #                 reader = csv.reader(file)
    #                 class_list = []
    #                 for i in range(3):
    #                     next(reader)
    #                 for line in reader:
    #                     if line[0] != '':
    #                         name = line[0].replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
    #                         first_name = name.split(' ')[-2]
    #                         class_list.append(first_name)
    #                 schedule[period] = class_list
    #         except:
    #             pass
    #     return schedule
