##### Bot libraries #####
from irc.bot import SingleServerIRCBot
from requests import get

import cmds
import react
from automod import clear

#### Database ####
import os
from sqlite3 import connect


base_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(base_dir, 'resources')
script_dir = os.path.join(base_dir, 'resources')

db = os.path.join(db_dir, 'database.db')
script = os.path.join(script_dir, 'script.sql')

cxn = connect(db, check_same_thread=False)
cur = cxn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner

@with_commit
def build():
    scriptexec(script)

def commit():
    cxn.commit()

def close():
    cxn.close()

def field(command, *values):
    cur.execute(command, tuple(values))

    if(fetch := cur.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))
    return cur.fetchall()

def column(command, *values):
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]

def execute(command, *values):
    cur.execute(command, tuple(values))

def multiexec(command, valueset):
    cur.executemany(command, valueset)

def scriptexec(filename):
    with open(filename, "r") as script:
        cur.executescript(script.read())

NAME = "<BotName>"
OWNER = "<OwnerName>"

class Bot(SingleServerIRCBot):
	def __init__(self):
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = "<ClientID>"
		self.TOKEN = "<BotToken>"
		self.CHANNEL = f"#{OWNER}"

		url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
		headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
		resp = get(url, headers=headers).json()
		self.channel_id = resp["users"][0]["_id"]

		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

	def on_welcome(self, cxn, event):
		for req in ("membership", "tags", "commands"):
			cxn.cap("REQ", f":twitch.tv/{req}")

		cxn.join(self.CHANNEL)
		build()
		self.send_message(f"{NAME} joined the chat.")
		self.status()

	@with_commit
	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		react.add_user(bot, user)

		if user["name"] != NAME and clear(bot, user, message):
			react.process(bot, user, message)
			cmds.process(bot, user, message)

	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)

	def status(self):
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("AwesomePyBot started successfully")
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
			print("**To shutdown the bot, close this window or use the command 'Ctrl + C'**")
			print("**If the bot doesn't start try reopening the program, that should fix the problem :D**")

if __name__ == "__main__":
    bot = Bot()
    bot.start()
