import datetime
import random

import matplotlib.pyplot as plt
from telebot.types import CallbackQuery

import telebot_calendar
import user_input
from Schedule.data import *
from config import *
from telebot_calendar import CallbackData

calendar = CallbackData("Schedule", "action", "year", "month", "day")


def schedule_date(message):
    now = datetime.datetime.now()
    markup = telebot_calendar.Calendar()
    markup = telebot_calendar.Calendar.create_calendar(
        self=markup,
        name=calendar.prefix,
        year=now.year,
        month=now.month,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Select schedule date",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar.prefix))
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar.sep)

    date = telebot_calendar.Calendar()
    date = telebot_calendar.Calendar.calendar_query_handler(self=date,
                                                            bot=bot, call=call, name=name, action=action, year=year,
                                                            month=month, day=day
                                                            )
    if action == "DAY":
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"You have chosen {date.strftime('%d.%m.%Y')}",
            reply_markup=user_input.default_markup(),
        )
        data_analysis(call.message, date.date())


def data_analysis(message, date):
    try:
        # database operations
        conn = sqlite3.connect(config.db_path)
        cursor = conn.cursor()
        script = f'''
        SELECT * FROM {config.db_table} WHERE id={message.chat.id}
        '''
        cursor.execute(script)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # db over
        # some shit
        x = []
        ylabels = []
        rows_name = []
        user_date = int(datetime.datetime(date.year, date.month, date.day, hour=0, minute=0, second=0).timestamp())

        # going through all data from db
        for row in rows:

            backet = str(row[2]).split("-")
            event_date = int(datetime.datetime(int(backet[0]),
                                               int(backet[1]),
                                               int(backet[2]),
                                               hour=0,
                                               minute=0,
                                               second=0).timestamp())

            if abs(int(event_date - user_date)) % row[6] == 0:
                print("ROW", row)
                rows_name.append(row[1])
                first = row[3]
                second = row[4]
                a = (first, second, row[1])
                x.append(a)

        # pyplot part
        fig, ax = plt.subplots()
        i = 0
        x.sort(key=lambda tup: tup[0], reverse=True)
        for m, evt in enumerate(x):
            start = int(evt[0].split(":")[0]) + ((int(evt[0].split(":")[1])) / 60)
            finish = ((int(evt[1].split(":")[1]) - int(evt[0].split(":")[1])) / 60) + (
                int(evt[1].split(":")[0])) - int(
                evt[0].split(":")[0]) + start

            if finish > start:

                ylabels.append(f'{evt[2]}\n'
                               f'{evt[0]} - {evt[1]}')

                ax.barh(i, width=finish - start, left=start, alpha=0.5)
                i += 1

            else:

                ylabels.append(f'{evt[2]}\n'
                               f'{evt[0]} - {evt[1]}')

                colors = ['b', 'r', 'k', 'y', 'm', 'c']
                clr = random.choice(colors)

                ax.barh(i, width=finish, left=0, alpha=0.5, color=clr)
                ax.barh(i, width=24 - start, left=start, alpha=0.5, color=clr)
                i += 1

        ax.set_yticks(range(len(ylabels)))
        ax.set_yticklabels(ylabels)
        ax.set_xticks(range(0, 25))
        ax.set_xticklabels(range(0, 25))
        ax.grid(False)
        plt.title = f"Schedule for {date}"
        fig = plt.gcf()
        fig.set_size_inches(19.2, 10.8)
        imagefile = f'Schedule/{message.chat.id}.png'
        plt.savefig(imagefile)
        img = open(imagefile, 'rb')
        bot.send_photo(message.chat.id, img, caption=f"Your schedule for {date}")
    except Exception as e:
        config.bot.send_message(message.chat.id, text=str(e))
