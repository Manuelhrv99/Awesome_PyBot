import main

def coins(bot, user, *args):
    coins = main.field("SELECT Coins FROM users WHERE UserID = ?",
        user["id"])
    bot.send_message(f"{user['name']}, you have {coins:,} coins.")