import os

import pandas as pd
import telebot

import config

bot = telebot.TeleBot(config.TOKEN)


def my_schedule(message):
    if os.stat("data.csv").st_size != 0:
        df = pd.read_csv("data.csv")
        data_id = df.query(f"id_client == {message.chat.id}")
        d_re = {}
        d_no_re = {}
        nl = "\n"
        for i in range(len(data_id)):
            if type(data_id["end_time"][i]) != str:
                if data_id["re"][i]:
                    d_re[f"{data_id['name_event'][i].replace('_', ' ')}: {data_id['start_time'][i]}"] = \
                        int(data_id["start_time"][i].split(":")[0]) + (
                                int(data_id["start_time"][i].split(":")[1]) / 100)
                else:
                    d_no_re[f"{data_id['name_event'][i].replace('_', ' ')}: {data_id['start_time'][i]}"] = \
                        int(data_id["start_time"][i].split(":")[0]) + (
                                int(data_id["start_time"][i].split(":")[1]) / 100)
            else:
                if data_id["re"][i]:
                    d_re[(f'{data_id["name_event"][i].replace("_", " ")}: '
                          f'{data_id["start_time"][i]} - {data_id["end_time"][i]}')] = \
                        int(str(data_id["start_time"][i]).split(":")[0]) + (
                                int(str(data_id["start_time"][i]).split(":")[1]) / 100)
                else:
                    d_no_re[(
                        f'{data_id["name_event"][i].replace("_", " ")}: {data_id["start_time"][i]} - '
                        f'{data_id["end_time"][i]}')] = \
                        int(data_id["start_time"][i].split(":")[0]) + (
                                int(data_id["start_time"][i].split(":")[1]) / 100)
        list_re = sort(d_re)
        list_no_re = sort(d_no_re)
        bot.send_message(message.chat.id, f"Repetitive events:{nl}"
                                          f"{nl}{f'{nl}'.join(list_re)}"
                                          f"{nl*2}Once-to-de events:{nl}"
                                          f"{nl}{f'{nl}'.join(list_no_re)}")
    else:
        bot.send_message(message.chat.id, "Your schedule is empty")


def sort(dictionary):
    list_d = list(dictionary.items())
    list_d.sort(key=lambda i: i[1])
    return [i[0] for i in list_d]
