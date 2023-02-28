import time
import datetime
from threading import Thread

from telebot import types

import config
import user_input
from Events import Sleeping, Eating, Custom_event
from Schedule import delete_event, data, schedule_img


@config.bot.message_handler(commands=['start'])
def welcome(message):
    markup = user_input.default_markup()
    config.bot.send_message(message.chat.id,
                            f"Welcome <b>{message.from_user.first_name}</b>!\n"
                            f"My name is <b>{config.bot.get_me().first_name}</b>\n"
                            f"Planck is an easy-to-use telegram bot to schedule your weekly"
                            f" routine by just answering simple questions)\n"
                            f"Let`s start",
                            parse_mode="html",
                            reply_markup=markup)


@config.bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.chat.type == 'private':
        if message.text == 'Add new event':
            markup = types.InlineKeyboardMarkup(row_width=2)
            sleeping = types.InlineKeyboardButton("Sleeping", callback_data='sleeping')
            eating = types.InlineKeyboardButton("Eating", callback_data='eating')
            own = types.InlineKeyboardButton("Custom event", callback_data='add')
            markup.add(sleeping, eating, own)
            config.bot.send_message(message.chat.id, 'What do we set up next?', reply_markup=markup)
        elif message.text == 'Today plans':
            schedule_img.data_analysis(message, datetime.datetime.now().date())
        elif message.text == "Weekly schedule":
            schedule_img.schedule_date(message)
        elif message.text == "Delete event":
            delete_event.select_event(message.chat.id)
        else:
            config.bot.send_message(message.chat.id,
                                    'Sorry, I dont understand you',
                                    reply_markup=user_input.default_markup())


@config.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'sleeping':
                config.bot.send_message(call.message.chat.id, "Fun fact: almost a third of life, you, humans, "
                                                              "spend sleeping\n"
                                                              "So let me ask you something about that:\n"
                                                              "When do you wake up?")
                config.bot.register_next_step_handler(call.message, Sleeping.get_up)
            elif call.data == 'eating':
                config.bot.send_message(call.message.chat.id, 'Eating')
                config.bot.send_message(call.message.chat.id, "Let me know, what time do you have breakfast?")
                config.bot.register_next_step_handler(call.message, Eating.breakfast)
            elif call.data == 'add':
                config.bot.send_message(call.message.chat.id, 'Lets create custom event for you: ')
                config.bot.send_message(call.message.chat.id, 'Send an event name: ')
                config.bot.register_next_step_handler(call.message, Custom_event.custom)

    except Exception as e:
        config.bot.send_message(call.message.chat.id, text=f"An error has occurred - {repr(e)}")


def run():
    while True:
        try:
            config.bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)


def main():
    data.init_db()
    Thread(target=run).start()
    Thread(target=user_input.schedule_per_user).start()


if __name__ == '__main__':
    main()
