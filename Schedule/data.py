import csv
import os

fieldnames = ["id_client", "name_event", "event_day", "start_time", "end_time", "re"]
filename = 'Schedule/data.csv'


def write(id_client, even, day, start_time, end_time, re):
    try:
        if os.stat(filename).st_size == 0:
            with open(filename, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        with open(filename, "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({"id_client": id_client,
                             "name_event": even,
                             "event_day": day,
                             "start_time": start_time,
                             "end_time": end_time,
                             "re": re})
    except FileNotFoundError:
        open(filename, "w")
        return write(id_client, even, day, start_time, end_time, re)
