import sqlite3

from telebot import types

import Schedule.data
import config


def select_event(user_id):
    rows = Schedule.data.select_all_user_events(user_id)
    reply_markup = types.InlineKeyboardMarkup(row_width=1)
    for row in rows:
        reply_markup.add(types.InlineKeyboardButton(f"Event {str(row[1])}", callback_data=f"Event_to_delete {row[1]}"))
    config.bot.send_message(chat_id=user_id, text="Select event to delete:", reply_markup=reply_markup)


@config.bot.callback_query_handler(func=lambda call: call.data.startswith("Event_to_delete"))
def cath_event_to_delete(call: types.CallbackQuery):
    event_name = str(call.data).replace('Event_to_delete ', '')
    config.bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
    config.bot.send_message(
        chat_id=call.from_user.id,
        text=f"You decided to delete event{event_name}"
    )
    delete_event_by_name(event_name)


def delete_event_by_name(name):
    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()
    sqlite3_del = f'''
    DELETE FROM {config.db_table} WHERE event="{name}"
    '''
    cursor.execute(sqlite3_del)
    conn.commit()
    conn.close()
