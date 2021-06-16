#Use this import in the virtual environmnet
#from fbs_runtime.application_context.PyQt5 import ApplicationContext

#GUI libraries
import sys
import os
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from py_toggle import PyToggle

#Bot libraries
from irc.bot import SingleServerIRCBot
from requests import get

from lib import db, cmds, react, automod

NAME = "TestBotPython"
OWNER = "manuelhrv99"

class Bot(SingleServerIRCBot):
	def __init__(self):
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = "kuj9eetu7jixx6rq55g54uj6ptedk0"
		self.TOKEN = "kvhoytzmtkb117fdyif85mx8t87erc"
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
		db.build()
		self.send_message(f"{NAME} joined the chat.")

	@db.with_commit
	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		react.add_user(bot, user)

		if user["name"] != NAME and automod.clear(bot, user, message):
			react.process(bot, user, message)
			cmds.process(bot, user, message)

	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #Resize MainWindow
        self.resize(400, 300)

        #Title of the window
        self.setWindowTitle("AwesomePyBot")

        #Create container and layout
        self.container = QFrame()
        self.container.setObjectName("container")
        self.container.setStyleSheet("#container { background-color: #222 }")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        #Adding the label
        self.label = QLabel("Off")
        self.label.setStyleSheet("color: #FFF; font-size: 50px; padding-top: 100px")
        self.layout.addWidget(self.label, Qt.AlignCenter, Qt.AlignCenter)

        #Add widget
        self.toggle = PyToggle()
        self.layout.addWidget(self.toggle, Qt.AlignCenter, Qt.AlignCenter)

        #Set central widget
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        #Show window
        self.show()

        #Change the text when the button is pressed
        self.toggle.stateChanged.connect(self.change_text)

    def change_text(self, value):
        if value:
            self.label.setText("On")
            bot.start()
        else:
            self.label.setText("Off")
            bot.send_message(f"{NAME} left the chat.")
            bot.stop()

if __name__ == "__main__":
    bot = Bot()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

#fbs's structure
"""if __name__ == "__main__":
        bot = Bot()
        appctxt = ApplicationContext()
        window = MainWindow()
        sys.exit(appctxt.app.exec())"""