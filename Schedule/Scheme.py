import os
from datetime import time as ch_time
import random
import matplotlib.pyplot as plt
import pandas as pd
import telebot

import config

bot = telebot.TeleBot(config.TOKEN)


def data_analysis(message):
    if os.stat("data.csv").st_size != 0:
        df = pd.read_csv("data.csv")
        data_id = df.query(f"id_client == {message.chat.id}")
        x = []
        ylabels = []
        print(data_id["name_event"])
        for i in range(len(data_id)):
            first = data_id["start_time"][i]
            second = data_id["end_time"][i]
            if not isinstance(data_id["end_time"][i], str):
                if int(first.split(":")[1]) + 20 <= 59:
                    second = ch_time(int(first.split(":")[0]), int(first.split(":")[1]) + 20)
                else:
                    delta = 20 - (60 - int(first.split(":")[1]))
                    second = ch_time(int(first.split(":")[0]) + 1, 0 + delta)
                if second.minute < 10 and second.hour < 10:
                    time_f = "0" + str(second.hour) + ":" + "0" + str(second.minute)
                elif second.minute < 10 < second.hour:
                    time_f = str(second.hour) + ":" + "0" + str(second.minute)
                elif second.minute > 10 > second.hour:
                    time_f = "0" + str(second.hour) + ":" + str(second.minute)
                else:
                    time_f = str(second.hour) + ":" + str(second.minute)
                a = (first, time_f)
            else:
                a = (first, second)
            x.append(a)

        fig, ax = plt.subplots()
        i = 0
        for m, evt in enumerate(x):
            start = int(evt[0].split(":")[0]) + ((int(evt[0].split(":")[1])) / 60)
            finish = ((int(evt[1].split(":")[1]) - int(evt[0].split(":")[1])) / 60) + (int(evt[1].split(":")[0])) - int(
                evt[0].split(":")[0]) + start
            timeline = list()
            if finish > start:
                timeline.append(start)
                timeline.append(finish - start)
                ylabels.append(f'{data_id["name_event"][i]}\n'
                               f'{evt[0]} - {evt[1]}')
                ax.barh(i, height=0.3, width=finish - start, left=start, alpha=0.5)
                i += 1
            else:
                timeline.append(start)
                timeline.append(finish - start)
                ylabels.append(f'{data_id["name_event"][i]}\n'
                               f'{evt[0]} - {evt[1]}')
                colors = ['w', 'b', 'r', 'k', 'y', 'm', 'c']
                clr = random.choice(colors)
                print(clr)
                ax.barh(i, height=0.3, width=finish, left=0, alpha=0.5, color=clr)
                ax.barh(i, height=0.3, width=24 - start, left=start, alpha=0.5, color=clr)
                i += 1

        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(ylabels)
        ax.set_xticks(range(0, 24))
        ax.set_xticklabels(range(0, 24))
        ax.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(19.2, 10.8)
        imagefile = 'data.png'
        plt.savefig(imagefile)
        img = open(imagefile, 'rb')
        bot.send_photo(message.chat.id, img)
    else:
        bot.send_message(message.chat.id, "Nothing to analyse so far(")
