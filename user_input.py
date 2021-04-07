import datetime
import time
from datetime import time as ch_time

import pandas as pd
from telebot import types

import Schedule.Scheme
from config import *


def error(message, function):
    bot.send_message(message.chat.id, "Try again: ")
    bot.register_next_step_handler(message, function)


def bot_send(row, name, day=None):
    # print("Inside bot send")
    bot.send_message(row.id_client, f"{name}", parse_mode='html')
    # else:
    #     bot.send_message(row.id_client, f"{name}", parse_mode='html')


def default_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Add new event")
    item2 = types.KeyboardButton("My schedule")
    item3 = types.KeyboardButton("My stats")
    item4 = 'debug_clear_csv'
    markup.add(item1, item2, item3, item4)
    return markup


def apologise(message):
    bot.send_message(message.chat.id, text="")
    pass


def user_time(message, function):
    text = message.text
    if ":" in text:
        try:
            time_dinner = ch_time(int(text.split(":")[0]), int(text.split(":")[1]))
        except ValueError:
            markup = default_markup()
            bot.send_message(message.chat.id, "Wrong input format", reply_markup=markup)
            error(message, function)
        else:
            return correct_time(time_dinner)

    else:
        try:
            time_dinner = int(text)
            if time_dinner < 10:
                time_dinner = "0" + str(time_dinner)
            time_dinner = str(time_dinner) + ":" + "0" * 2
            return time_dinner
        except ValueError:
            markup = default_markup()
            bot.send_message(message.chat.id, "Wrong input format", reply_markup=markup)
            error(message, function)


def end_time(start_time, delta_time):
    hours = int(start_time.split(":")[0])
    minutes = int(start_time.split(":")[1])
    minutes_sum = minutes + delta_time
    if minutes_sum > 59:
        minutes = minutes_sum - 60
        hours += 1
        if hours == 24:
            hours = 0
    else:
        minutes = minutes_sum
    time_dinner = ch_time(hours, minutes)
    return correct_time(time_dinner)


def correct_time(time_dinner):
    if time_dinner.minute < 10 and time_dinner.hour < 10:
        time_f = "0" + str(time_dinner.hour) + ":" + "0" + str(time_dinner.minute)
    elif time_dinner.minute < 10 <= time_dinner.hour:
        time_f = str(time_dinner.hour) + ":" + "0" + str(time_dinner.minute)
    elif time_dinner.minute >= 10 > time_dinner.hour:
        time_f = "0" + str(time_dinner.hour) + ":" + str(time_dinner.minute)
    else:
        time_f = str(time_dinner.hour) + ":" + str(time_dinner.minute)
    return time_f


def schedule_per_user():
    while True:
        df = pd.read_csv(Schedule.Scheme.filename)
        cur_time = datetime.datetime.now()
        cur_time_1970 = datetime.datetime(year=cur_time.year,
                                          month=cur_time.month,
                                          day=cur_time.day,
                                          hour=cur_time.hour,
                                          minute=cur_time.minute,
                                          second=cur_time.second).timestamp()
        for row in df.itertuples():
            row_date = str(row.event_day).split("-")
            row_time = str(row.start_time).split(":")
            row_1970 = datetime.datetime(year=int(row_date[0]),
                                         month=int(row_date[1]),
                                         day=int(row_date[2]),
                                         hour=int(row_time[0]),
                                         minute=int(row_time[1]),
                                         second=0
                                         ).timestamp()
            if (abs(int(cur_time_1970 - row_1970)) % row.delta == 0 and row.re is True) or\
                    (cur_time_1970 == row_1970 and row.re is False):
                bot_send(row,
                         f"Time for event <b>{row.name_event}</b>\n"
                         f"{row.start_time} - {row.end_time}",
                         row.event_day)
        time.sleep(1)
