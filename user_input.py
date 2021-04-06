import datetime
import time
from datetime import time as ch_time

import schedule
from telebot import types

from config import *


def error(message, function):
    bot.send_message(message.chat.id, "Try again: ")
    bot.register_next_step_handler(message, function)


def bot_send(message, name, day=None):
    if day is not None:
        if day == datetime.datetime.now().date():
            bot.send_message(message.chat.id, f"{name}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, f"{name}", parse_mode='html')


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


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)
