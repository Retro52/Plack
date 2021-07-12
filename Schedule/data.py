import csv
import os
import config


def write(id_client, even, day, start_time, end_time, re, delta):
    try:
        if os.stat(config.filename).st_size == 0:
            with open(config.filename, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=config.fieldnames)
                writer.writeheader()
        with open(config.filename, "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=config.fieldnames)
            writer.writerow({"id_client": id_client,
                             "name_event": even,
                             "event_day": day,
                             "start_time": start_time,
                             "end_time": end_time,
                             "re": re,
                             "delta": delta})
    except FileNotFoundError:
        open(config.filename, "w")
        return write(id_client, even, day, start_time, end_time, re, delta)
