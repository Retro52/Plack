from Events.Custom_event import *

new_event = CustomEvent()


def get_up(message):
    try:
        new_event.__init__()
        new_event.id_clients = message.chat.id
        new_event.event = "Sleeping"
        time_get_up = user_time(message, get_up)
        if time_get_up:
            bot.send_message(message.chat.id, f"Okay, so you wake up at {time_get_up}. Huh, interesting.\n"
                                              f"Let me know, when you go to bed?")
            new_event.end_time = time_get_up
            new_event.re = True
            bot.register_next_step_handler(message, got_to_bed)
    except ValueError:
        error(message, get_up)


def got_to_bed(message):
    try:
        time_go_to_bed = user_time(message, got_to_bed)
        if time_go_to_bed:
            bot.send_message(message.chat.id, f"Okay, you go to bed at {time_go_to_bed}. Hmm, that`s interesting.\n"
                                              f"I think we're done here.\nNow you can set up another part of your life")
            new_event.start_time = time_go_to_bed
            new_event.create()
        else:
            apologise(message)
    except ValueError:
        error(message, got_to_bed)
