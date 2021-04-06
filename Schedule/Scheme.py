import random

import matplotlib.pyplot as plt
import pandas as pd
from telebot.types import CallbackQuery

import telebot_calendar
from Schedule.data import *
from telebot_calendar import CallbackData
from user_input import *

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
            reply_markup=default_markup(),
        )
        data_analysis(call.message, date.date())


def data_analysis(message, date):
    try:
        if os.stat(filename).st_size != 0:
            df = pd.read_csv(filename)
            data_id = df.query(f"id_client ==  {message.chat.id}")
            x = []
            ylabels = []
            rows_name = []
            for row in data_id.itertuples():
                if str(row.event_day) == 'nan' or row.event_day == str(date):
                    print("ROW", row)
                    rows_name.append(row.name_event)
                    first = row.start_time
                    second = row.end_time
                    a = (first, second)
                    x.append(a)

            fig, ax = plt.subplots()
            i = 0
            for m, evt in enumerate(x):

                start = int(evt[0].split(":")[0]) + ((int(evt[0].split(":")[1])) / 60)
                finish = ((int(evt[1].split(":")[1]) - int(evt[0].split(":")[1])) / 60) + (
                    int(evt[1].split(":")[0])) - int(
                    evt[0].split(":")[0]) + start

                if finish > start:

                    ylabels.append(f'{rows_name[i]}\n'
                                   f'{evt[0]} - {evt[1]}')

                    ax.barh(i, width=finish - start, left=start, alpha=0.5)
                    # ax.barh(i, height=0.3, width=finish - start, left=start, alpha=0.5)
                    i += 1

                else:
                    print("ROW NAME", f'{rows_name[i]}\n'
                          f'{evt[0]} - {evt[1]}')

                    ylabels.append(f'{rows_name[i]}\n'
                                   f'{evt[0]} - {evt[1]}')

                    colors = ['b', 'r', 'k', 'y', 'm', 'c']
                    clr = random.choice(colors)

                    ax.barh(i, width=finish, left=0, alpha=0.5, color=clr)
                    # ax.barh(i, height=0.3, width=finish, left=0, alpha=0.5, color=clr)
                    ax.barh(i, width=24 - start, left=start, alpha=0.5, color=clr)
                    # ax.barh(i, height=0.3, width=24 - start, left=start, alpha=0.5, color=clr)
                    i += 1

            ax.set_yticks(range(len(ylabels)))
            ax.set_yticklabels(ylabels)
            ax.set_xticks(range(0, 25))
            ax.set_xticklabels(range(0, 25))
            # ax.grid(True)
            ax.grid(False)
            plt.title = f"Schedule for {date}"
            fig = plt.gcf()
            fig.set_size_inches(19.2, 10.8)
            imagefile = 'Schedule/data.png'
            plt.savefig(imagefile)
            img = open(imagefile, 'rb')
            bot.send_photo(message.chat.id, img, caption=f"Your schedule for {date}")
        else:
            bot.send_message(message.chat.id, "Nothing to analyse so far(")
    except FileNotFoundError:
        open(filename, "w")
        return data_analysis(message, date)
