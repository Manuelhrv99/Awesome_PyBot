import main

CURSES = ("bum", "poo", "you are bad")
warning_timers = (1, 5, 60)

def clear(bot, user, message):
    #Automatization of messages
    if "Hi" in message:
        bot.send_message(f"Hi! {user['name']}. PunOko PunOko PunOko")
    if "clear" in message:
        bot.send_message("/clear")

    if any([curse in message for curse in CURSES]):
        warn(bot, user, reason="Cursing")
        return False

    return True

def warn(bot, user, *, reason=None):
    warnings = main.field("SELECT Warnings FROM users WHERE UserID = ?",
        user["id"])

    if warnings < len(warning_timers):
        mins = warning_timers[warnings]
        bot.send_message(f"/timeout {user['name']} {mins}m")
        bot.send_message(f"{user['name']}, you have been muted for the following reason: {reason}. You will be unmuted in {mins} minute(s).")

        main.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?",
            user["id"])
    else:
        bot.send_message(f"/ban {user['name']} Repeated infractions.")
        bot.send_message(f"{user['name']}, you have been banned from chat for repeated infractions.")