import time
from datetime import time as ch_time
import schedule
import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)


def error(message, function):
    bot.send_message(message.chat.id, "Try again: ")
    bot.register_next_step_handler(message, function)


def bot_send(message, name):
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
            if time_dinner.minute < 10 and time_dinner.hour < 10:
                time_f = "0" + str(time_dinner.hour) + ":" + "0" + str(time_dinner.minute)

            elif time_dinner.minute < 10 <= time_dinner.hour:
                time_f = str(time_dinner.hour) + ":" + "0" + str(time_dinner.minute)
            elif time_dinner.minute >= 10 > time_dinner.hour:
                time_f = "0" + str(time_dinner.hour) + ":" + str(time_dinner.minute)
            else:
                time_f = str(time_dinner.hour) + ":" + str(time_dinner.minute)
            print(time_f)
            return time_f

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


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)
