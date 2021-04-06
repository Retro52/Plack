from Events.Custom_event import *


def breakfast(message):
    try:
        time_breakfast = user_time(message, breakfast)
        if time_breakfast:
<<<<<<< HEAD
=======
            # schedule.every().days.at(time_breakfast).do(bot_send, message, "Time for breakfast\nBon appetit! ")
>>>>>>> 6e096c8030ea05dd29c32a26fffdb15721f5dff3
            bot.send_message(message.chat.id, f"You have a breakfast at {time_breakfast}. Noted✔")
            bot.send_message(message.chat.id, f"What time do you have lunch?")
            new_event.__init__()
            new_event.id_clients = message.chat.id
            new_event.event = "Breakfast"
            new_event.re = True
            new_event.start_time = time_breakfast
            new_event.end_time = end_time(new_event.start_time, 30)
            new_event.create()
            bot.register_next_step_handler(message, lunch)
    except ValueError:
        error(message, breakfast)


def lunch(message):
    try:
        time_lunch = user_time(message, lunch)
        if time_lunch:
<<<<<<< HEAD
=======
            # schedule.every().days.at(time_lunch).do(bot_send, message,
            #                                         "I wish i could eat lunch, but I am just a bot...\n"
            #                                         "Go feed yourself")
>>>>>>> 6e096c8030ea05dd29c32a26fffdb15721f5dff3
            bot.send_message(message.chat.id, f"You have a lunch at {time_lunch}. Well, well, well...")
            bot.send_message(message.chat.id, f"What time do you have dinner?")
            new_event.__init__()
            new_event.id_clients = message.chat.id
            new_event.event = "Lunch"
            new_event.re = True
            new_event.start_time = time_lunch
            new_event.end_time = end_time(new_event.start_time, 30)
            new_event.create()
            bot.register_next_step_handler(message, dinner)
    except ValueError:
        error(message, lunch)


def dinner(message):
    try:
        time_dinner = user_time(message, dinner)
        if time_dinner:
<<<<<<< HEAD
=======
            # schedule.every().days.at(time_dinner).do(bot_send, message, f"Time for some delicious food.\n"
            #                                                             "If you are interested in my opinion,"
            #                                                             " I prefer some good sorted data."
            #                                                             "\n\n\n\n\n\n\n"
            #                                                             "P.S. There"
            #                                                             " could be an add of your restaurant\n")
>>>>>>> 6e096c8030ea05dd29c32a26fffdb15721f5dff3
            new_event.__init__()
            new_event.id_clients = message.chat.id
            new_event.event = "Diner"
            new_event.re = True
            new_event.start_time = time_dinner
            new_event.end_time = end_time(new_event.start_time, 30)
            new_event.create()
            bot.send_message(message.chat.id,
                             f"You have a dinner at {time_dinner}. \nNow I will send this to server where"
                             f"special algorithms will be analyzing this data (no). "
                             f"\nBtw, you can set up something else")
        else:
            apologise(message)
    except ValueError:
        error(message, dinner)
