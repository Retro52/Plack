from Schedule import data
from user_input import *


class CustomEvent:
    def __init__(self):
        """Custom event"""
        self.id_clients = None
        self.event = "Event"
        self.start_time = None
        self.end_time = None
        self.re = False
        self.delta = None

    def create(self):
        data.write(self.id_clients, self.event, self.start_time, self.end_time, self.re, self.delta)


new_event = CustomEvent()


def custom(message):
    new_event.__init__()
    new_event.id_clients = message.chat.id
    new_event.event = message.text
    bot.register_next_step_handler(message, custom_start_time)
    bot.send_message(message.chat.id, "Now send start time: ")


def custom_start_time(message):
    new_event.start_time = user_time(message, custom_start_time)
    if new_event.start_time:
        bot.register_next_step_handler(message, custom_end_time)
        bot.send_message(message.chat.id, "Now send end time: ")


def custom_end_time(message):
    new_event.end_time = user_time(message, custom_end_time)
    if new_event.end_time:
        markup_custom = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Yes")
        item2 = types.KeyboardButton("No, thanks")
        markup_custom.add(item1, item2)
        bot.register_next_step_handler(message, finish_custom)
        bot.send_message(message.chat.id, "Final question: would you like to make this event repetitive time: ",
                         reply_markup=markup_custom)


def finish_custom(message):
    if message.text == 'Yes':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Every day")
        item2 = types.KeyboardButton("Every week")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Select a repeat frequency: ", reply_markup=markup)
        new_event.re = True
        bot.register_next_step_handler(message, custom_period)
    elif message.text == 'No, thanks':
        markup = default_markup()
        bot.send_message(message.chat.id, "Understandable, have a nice day)", reply_markup=markup)
        new_event.re = False
        print(new_event.start_time)
        print(new_event.end_time)
        new_event.create()
        schedule.every().days.at(new_event.start_time).do(bot_send, message,
                                                          f"Time for event <b>{new_event.event}</b>\n"
                                                          f"{new_event.start_time} - {new_event.end_time}")
    else:
        bot.send_message(message.chat.id, "Please, select option from the keyboard: ")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Yes")
        item2 = types.KeyboardButton("No, thanks")
        markup.add(item1, item2)
        bot.register_next_step_handler(message, finish_custom)
        bot.send_message(message.chat.id, "Same question: would you like to make this event repetitive time: ",
                         reply_markup=markup)


def custom_period(message):
    if message.text == "Every day":
        new_event.delta = 1
        new_event.create()
        schedule.every().days.at(new_event.start_time).do(bot_send, message,
                                                          f"Time for event <b>{new_event.event}</b>\n"
                                                          f"{new_event.start_time} - {new_event.end_time}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add new event")
        item2 = types.KeyboardButton("My schedule")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, f"Event <b>{new_event.event}</b> successfully created",
                         parse_mode='html', reply_markup=markup)
    elif message.text == "Every week":
        new_event.delta = 7
        new_event.create()
        schedule.every().days.at(new_event.start_time).do(bot_send, message,
                                                          f"Time for event <b>{new_event.event}</b>\n"
                                                          f"{new_event.start_time} - {new_event.end_time}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Add new event")
        item2 = types.KeyboardButton("My schedule")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Event successfully created", reply_markup=markup)
    else:
        error(message, custom_period)
