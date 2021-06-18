from collections import defaultdict
from re import search
from datetime import datetime, timedelta
from random import randint
from time import time

import main
import games

welcomed = []
messages = defaultdict(int)

hello_list = ("Say hi to", "Hail to", "This land is cursed now by", "Oni San UwU", "Take this ( •_•)>⌐■-■")

def process(bot, user, message):
	update_records(bot, user)

	if user["id"] not in welcomed:
		welcome(bot, user)
	elif "bye" in message:
		say_goodbye(bot, user)

	check_activity(bot, user)

	if (match := search(r'cheer[0-9]+', message)) is not None:
		thank_for_cheer(bot, user, match)

	if (h := games.heist) is not None:
		if h.start_time <= time() and not h.running:
			games.run_heist(bot)
		elif h.end_time <= time() and h.running:
			games.end_heist(bot)

def add_user(bot, user):
    main.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?, ?)",
        user["id"], user["name"].lower())


def update_records(bot, user):
    main.execute("UPDATE users SET UserName = ?, MessageSent = MessageSent + 1 WHERE UserID = ?",
        user["name"].lower(), user["id"])

    stamp = main.field("SELECT CoinLock FROM users WHERE UserID = ?",
        user["id"])

    if datetime.strptime(stamp,"%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow() + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        
        main.execute("UPDATE users SET Coins = Coins + ?, CoinLock = ? WHERE UserID = ?",
            randint(1, 5), coinlock, user["id"])

#Messages when enter or leave the chat
def welcome(bot, user):
    bot.send_message(f"{hello_list[randint(0, 4)]} {user['name']} TPFufun TPFufun")
    welcomed.append(user["id"])

def say_goodbye(bot, user):
    bot.send_message(f"See you later {user['name']}!")
    welcomed.remove(user["id"])

def check_activity(bot, user):
    messages[user["id"]] += 1

    if(count := messages[user["id"]]) % 3 == 0:
        bot.send_message(f"Thanks to the user {user['name']} for being active in the chat. You have sent {count:,} messages! Keep it up!")

def thank_for_cheer(bot, user, match):
    bot.send_message(f"Thanks for the {match.group[5:]:,} bits {user['name']}! That's really appreciated.")