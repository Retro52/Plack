from telebot.types import ReplyKeyboardRemove, CallbackQuery

import telebot_calendar
from Schedule import data
from telebot_calendar import CallbackData
from user_input import *

calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")


class CustomEvent:
    def __init__(self):
        """Custom event"""
        self.id_clients = None
        self.event = "Event"
        self.start_time = None
        self.end_time = None
        self.re = False
        self.day = None

    def create(self):
        data.write(self.id_clients, self.event, self.day, self.start_time, self.end_time, self.re)


new_event = CustomEvent()


def custom(message):
    new_event.__init__()
    new_event.id_clients = message.chat.id
    new_event.event = message.text
    now = datetime.datetime.now()
    markup = telebot_calendar.Calendar()
    markup = telebot_calendar.Calendar.create_calendar(
        self=markup,
        name=calendar_1.prefix,
        year=now.year,
        month=now.month,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Select event date",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)

    date = telebot_calendar.Calendar()
    date = telebot_calendar.Calendar.calendar_query_handler(self=date,
                                                            bot=bot, call=call, name=name, action=action, year=year,
                                                            month=month, day=day
                                                            )

    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"You have chosen {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove(),
        )
        new_event.day = date.date()
        # new_event.day = new_event.day.strftime('%m/%d/%Y')
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"Now send event start time (for example '11:00' or just '11')",
            reply_markup=default_markup(),

        )
        bot.register_next_step_handler(call.message, custom_start_time)
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Event creation canceled",
            reply_markup=default_markup(),
        )


def custom_start_time(message):
    new_event.start_time = user_time(message, custom_start_time)
    if new_event.start_time:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Now send event end time (for example '20:00' or just '20')",
            reply_markup=default_markup(),
        )
        bot.register_next_step_handler(message, custom_end_time)


def custom_end_time(message):
    new_event.end_time = user_time(message, custom_end_time)
    if new_event.end_time:
        markup = default_markup()
        bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
        new_event.re = False
        print(new_event.start_time)
        print(new_event.end_time)
        schedule.every().days.at(new_event.start_time).do(bot_send, message,
                                                          f"Time for event <b>{new_event.event}</b>\n"
                                                          f"{new_event.start_time} - {new_event.end_time}",
                                                          new_event.day)
        new_event.create()


# def finish_custom(message):
#     if message.text == 'Yes':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         item1 = types.KeyboardButton("Every day")
#         item2 = types.KeyboardButton("Every week")
#         markup.add(item1, item2)
#         bot.send_message(message.chat.id, "Select a repeat frequency: ", reply_markup=markup)
#         new_event.re = True
#         bot.register_next_step_handler(message, custom_period)
#     elif message.text == 'No, thanks':
#         markup = default_markup()
#         bot.send_message(message.chat.id, "Understandable, have a nice day)", reply_markup=markup)
#         new_event.re = False
#         print(new_event.start_time)
#         print(new_event.end_time)
#         new_event.create()
#         schedule.every().days.at(new_event.start_time).do(bot_send, message,
#                                                           f"Time for event <b>{new_event.event}</b>\n"
#                                                           f"{new_event.start_time} - {new_event.end_time}",
#                                                           new_event.day)
#     else:
#         bot.send_message(message.chat.id, "Please, select option from the keyboard: ")
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         item1 = types.KeyboardButton("Yes")
#         item2 = types.KeyboardButton("No, thanks")
#         markup.add(item1, item2)
#         bot.register_next_step_handler(message, finish_custom)
#         bot.send_message(message.chat.id, "Same question: would you like to make this event repetitive time: ",
#                          reply_markup=markup)
#
#
# def custom_period(message):
#     if message.text == "Every day":
#         new_event.delta = 1
#         new_event.create()
#         schedule.every().days.at(new_event.start_time).do(bot_send, message,
#                                                           f"Time for event <b>{new_event.event}</b>\n"
#                                                           f"{new_event.start_time} - {new_event.end_time}")
#         markup = default_markup()
#         bot.send_message(message.chat.id, f"Event <b>{new_event.event}</b> successfully created",
#                          parse_mode='html', reply_markup=markup)
#     elif message.text == "Every week":
#         new_event.delta = 7
#         new_event.create()
#         schedule.every().days.at(new_event.start_time).do(bot_send, message,
#                                                           f"Time for event <b>{new_event.event}</b>\n"
#                                                           f"{new_event.start_time} - {new_event.end_time}")
#         markup = default_markup()
#         bot.send_message(message.chat.id, "Event successfully created", reply_markup=markup)
#     else:
#         error(message, custom_period)
