import csv
import config
import pandas as pd


def delete(event_name, user):
    print(user)
    df = pd.read_csv(config.filename)
    print(df)
    data_id = df.query(f"id_client == {user}")
    print(data_id)
    data_id = data_id.query(f"name_event != Sleeping")
    print(data_id)
    data_id.to_csv("test.csv")


