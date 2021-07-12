from telebot.types import ReplyKeyboardRemove, CallbackQuery

import telebot_calendar
from Schedule import data
from telebot_calendar import CallbackData
from user_input import *
from config import *

calendar_1 = CallbackData("CustomEventDate", "action", "year", "month", "day")


class CustomEvent:
    def __init__(self):
        """Custom event"""
        self.id_clients = None
        self.event = "Event"
        self.day = str(datetime.datetime.now().date())
        self.start_time = None
        self.end_time = None
        self.re = False
        self.delta = None

    def create(self):
        data.write(self.id_clients, self.event, self.day, self.start_time, self.end_time, self.re, self.delta)


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
        print(new_event.start_time)
        print(new_event.end_time)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Once a week")
        item2 = types.KeyboardButton("Every day")
        item3 = types.KeyboardButton("No, thanks")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, f"Is this event repetitive?\n"
                                          f"If yes, you can send a number of days between this event or pick"
                                          f"from the prepared buttons\n"
                                          f"For example, if you want to repeat it once a week send 7.\n"
                                          f"Every day - 1, etc.", reply_markup=markup)
        bot.register_next_step_handler(message, custom_repeat)


def custom_repeat(message):
    if message.text == "Once a week":
        new_event.re = True
        new_event.delta = 7 * 24 * 60 * 60
        markup = default_markup()
        bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
        new_event.create()
    elif message.text == "Every day":
        new_event.re = True
        new_event.delta = 1 * 24 * 60 * 60
        markup = default_markup()
        bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
        new_event.create()
    elif message.text == "No, thanks":
        new_event.re = False
        markup = default_markup()
        bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
        new_event.create()
    else:
        try:
            delta = int(message.text)
            if delta == 1:
                new_event.re = False
                new_event.delta = delta
                new_event.day = None
                markup = default_markup()
                bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
                new_event.create()
            else:
                new_event.re = True
                new_event.delta = delta * 24 * 60 * 60
                markup = default_markup()
                bot.send_message(message.chat.id, f"Event {new_event.event} successfully created", reply_markup=markup)
                new_event.create()

        except ValueError:
            bot.send_message(message.chat.id, "Sorry, didn`t get what you mean")
            error(message, custom_repeat)
