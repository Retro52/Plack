import collections

import pandas as pd

from Schedule.data import *
from config import *


def my_schedule(message):
    try:
        print(os.stat(filename))
        if os.stat(filename).st_size != 0:
            df = pd.read_csv(filename)
            data_id = df.query(f"id_client == {message.chat.id}")
            dates_dict = {}
            for row in data_id.itertuples():
                dates_dict[str(row.name_event)] = str(row.event_day), f"{row.start_time} - {row.end_time}"
                print(type(dates_dict[str(row.name_event)]))
            dates_dict = collections.OrderedDict(sorted(dates_dict.items(), key=lambda x: x[1], reverse=False))
            print(dates_dict)
            text = "Custom tasks: \n\n"
            for data in dates_dict:
                if dates_dict[data][0] != 'nan':
                    text += "{:<30} {:<30} {:<30}\n".format(data, dates_dict[data][0], dates_dict[data][1])
            text += "\nRoutine tasks: \n\n"
            for data in dates_dict:
                if dates_dict[data][0] == 'nan':
                    text += "{:<30} {:<30} {:<30}\n".format(data, "Routine task", dates_dict[data][1])
            print(text)
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Your schedule is empty")
    except FileNotFoundError:
        open(filename, "w")
        return my_schedule(message)


def sort(dictionary):
    list_d = list(dictionary.items())
    list_d.sort(key=lambda i: i[1])
    return [i[0] for i in list_d]
