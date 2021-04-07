from threading import Thread

from Schedule import schedule_print as sch, Scheme
from Events.Sleeping import *
from Events.Eating import *
# from user_input import *


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = default_markup()

    bot.send_message(message.chat.id,
                     f"Welcome <b>{message.from_user.first_name}</b>!\nMy name is <b>{bot.get_me().first_name}</b>\n"
                     f"Planck is an easy-to-use telegram bot to schedule your weekly"
                     f" routine by just answering simple questions)\n"
                     f"Let`s start",
                     parse_mode="html",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.chat.type == 'private':

        if message.text == 'Add new event':

            markup = types.InlineKeyboardMarkup(row_width=2)

            item1 = types.InlineKeyboardButton("Sleeping", callback_data='sleeping')
            item2 = types.InlineKeyboardButton("Eating", callback_data='eating')
            item3 = types.InlineKeyboardButton("Trainings", callback_data='trainings')
            item4 = types.InlineKeyboardButton("Pets", callback_data='pets')
            item5 = types.InlineKeyboardButton("Cleaning", callback_data='cleaning')
            item6 = types.InlineKeyboardButton("Studying/working hours", callback_data='studying')
            item7 = types.InlineKeyboardButton("Self-education", callback_data='education')
            item8 = types.InlineKeyboardButton("Add something new   ", callback_data='add')

            markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

            bot.send_message(message.chat.id, 'What do we set up next, boss?', reply_markup=markup)
        elif message.text == 'My schedule':
            sch.my_schedule(message)
        elif message.text == "My stats":
            Scheme.schedule_date(message)
        elif message.text == 'debug_clear_csv':
            filename = "Schedule/data.csv"
            f = open(filename, "w+")
            f.close()
        else:
            bot.send_message(message.chat.id, 'Sorry, I dont understand you')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'sleeping':
                bot.send_message(call.message.chat.id, "Fun fact: almost a third of life, you, humans, "
                                                       "spend sleeping\n"
                                                       "So let me ask you something about that:\n"
                                                       "When do you wake up?")
                bot.register_next_step_handler(call.message, get_up)
            elif call.data == 'eating':
                bot.send_message(call.message.chat.id, 'Eating')
                bot.send_message(call.message.chat.id, "Let me know, what time do you have breakfast?")
                bot.register_next_step_handler(call.message, breakfast)
            elif call.data == 'trainings':
                bot.send_message(call.message.chat.id, 'Trainings')
            elif call.data == 'pets':
                bot.send_message(call.message.chat.id, 'Pets')
            elif call.data == 'cleaning':
                bot.send_message(call.message.chat.id, 'Cleaning')
            elif call.data == 'studying':
                bot.send_message(call.message.chat.id, 'Studying')
            elif call.data == 'education':
                bot.send_message(call.message.chat.id, 'Education')
            elif call.data == 'add':
                bot.send_message(call.message.chat.id, 'Lets create custom event for you: ')
                bot.send_message(call.message.chat.id, 'Enter event name: ')
                bot.register_next_step_handler(call.message, custom)
            elif call.data in "123456789101112131415161718192021222324":
                bot.send_message(call.message.chat.id, f"Okay {call.data}")

    except Exception as e:
        bot.send_message(call.message.chat.id, text=f"An error has occurred - {repr(e)}")


def main():
    # Thread(target=schedule_checker).start()
    Thread(target=schedule_per_user).start()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
