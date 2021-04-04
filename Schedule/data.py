import csv
import os

fieldnames = ["id_client", "name_event", "start_time", "end_time", "re", "delta_time"]


def write(id_client, even, start_time, end_time, re, delta_time):
    if os.stat("data.csv").st_size == 0:
        with open("data.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    with open("data.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow({"id_client": id_client,
                         "name_event": even,
                         "start_time": start_time,
                         "end_time": end_time,
                         "re": re,
                         "delta_time": delta_time})
