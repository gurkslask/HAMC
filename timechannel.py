__author__ = 'alexander'

import datetime as dt


class timechannel(object):
    def __init__(self):
        self.time_dict = {
            0: [], # 'monday': [(dt.time(18, 00), True), (dt.time(20, 00), False)],
            1: [], # 'tuesday': [],
            2: [], # 'wednesday': [],
            3: [], # 'thursday': [],
            4: [], # 'friday': [],
            5: [], # 'saturday': [],
            6: [] # 'sunday': []
        }

    def check_state(self):
        hour = int(dt.datetime.today().strftime('%H'))
        minute = int(dt.datetime.today().strftime('%M'))
        act_time = dt.time(hour, minute)
        #Load different values for different weekdays
        act_times = self.time_dict[dt.date.weekday(dt.datetime.today())]
        act_times.sort(key=lambda r: r[0])
        keys = [r[0] for r in act_times]
        for pos, data in enumerate(keys):
            if data > act_time:
                return act_times[pos-1][1]
        return False


    def check_if_true_test(self, hour, minute, day):
        act_time = dt.time(hour, minute)
        #Load different values for different weekdays
        act_times = self.time_dict[day]
        act_times.sort(key=lambda r: r[0])
        keys = [r[0] for r in act_times]
        for pos, data in enumerate(keys):
            if data > act_time:
                return act_times[pos-1][1]
        return False

