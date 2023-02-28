import datetime
import time
from datetime import time as ch_time

from telebot import types

import Schedule.data
import Schedule.schedule_img
import config


def error(message, function):
    config.bot.send_message(message.chat.id, "Try again: ")
    config.bot.register_next_step_handler(message, function)


def bot_send(user_id, message):
    config.bot.send_message(user_id, f"{message}", parse_mode='html')


def default_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Add new event")
    item2 = types.KeyboardButton("Today plans")
    item3 = types.KeyboardButton("Weekly schedule")
    item4 = types.KeyboardButton("Delete event")
    markup.add(item1, item2, item3, item4)
    return markup


def apologise(message):
    config.bot.send_message(message.chat.id, text="")
    pass


def user_time(message, function):
    text = message.text
    if ":" in text:
        try:
            user_input_time = ch_time(int(text.split(":")[0]), int(text.split(":")[1]))
        except ValueError:
            markup = default_markup()
            config.bot.send_message(message.chat.id, "Wrong input format", reply_markup=markup)
            error(message, function)
        else:
            return correct_time(user_input_time)

    else:
        try:
            user_input_time = int(text)
            if user_input_time < 0 or user_input_time > 23:
                raise ValueError
            if user_input_time < 10:
                user_input_time = "0" + str(user_input_time)
            if user_input_time == 24:
                user_input_time = 0
            user_input_time = str(user_input_time) + ":" + "0" * 2
            return user_input_time
        except ValueError:
            markup = default_markup()
            config.bot.send_message(message.chat.id, "Wrong input format", reply_markup=markup)
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


def correct_time(time_to_check):
    if time_to_check.minute < 10 and time_to_check.hour < 10:
        time_f = "0" + str(time_to_check.hour) + ":" + "0" + str(time_to_check.minute)
    elif time_to_check.minute < 10 <= time_to_check.hour:
        time_f = str(time_to_check.hour) + ":" + "0" + str(time_to_check.minute)
    elif time_to_check.minute >= 10 > time_to_check.hour:
        time_f = "0" + str(time_to_check.hour) + ":" + str(time_to_check.minute)
    else:
        time_f = str(time_to_check.hour) + ":" + str(time_to_check.minute)
    return time_f


def schedule_per_user():
    while True:
        cur_time = datetime.datetime.now()
        rows = Schedule.data.select_all_events()
        cur_time_1970 = datetime.datetime(year=cur_time.year,
                                          month=cur_time.month,
                                          day=cur_time.day,
                                          hour=cur_time.hour,
                                          minute=cur_time.minute,
                                          second=cur_time.second).timestamp()
        for row in rows:
            row_date = str(row[2]).split("-")
            row_time = str(row[3]).split(":")
            row_1970 = datetime.datetime(year=int(row_date[0]),
                                         month=int(row_date[1]),
                                         day=int(row_date[2]),
                                         hour=int(row_time[0]),
                                         minute=int(row_time[1]),
                                         second=0
                                         ).timestamp()
            if abs(int(cur_time_1970 - row_1970)) % row[6] == 0:
                bot_send(row[0],
                         f"Time for event <b>{row[1]}</b>\n"
                         f"{row[3]} - {row[4]}")
        b = datetime.datetime.now()
        a = 1 - (b - cur_time).total_seconds()
        time.sleep(a)
