# awesomePyBot

## Setup for the virtual environment

> 1st Step

Open a command prompt in your project directory and execute the following:

`%LOCALAPPDATA%\Programs\Python\Python39\python -m venv venv`

`call venv\Scripts\activate.bat`

> 2nd Step

Install the libraries.

`pip install fbs, PyQt5, PySide6, irc, requests, sqlite3, collections, re, datetime, random, time`

> 3rd Step

Test that the app still works.

> 4th Step

Convert to fbs's project structure.

Replace

    if __name__ == "__main__":
        bot = Bot()
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec())

With

    if __name__ == "__main__":
        bot = Bot()
        appctxt = ApplicationContext()
        window = MainWindow()
        sys.exit(appctxt.app.exec())

`fbs startproject`

After the creation of the folders move main.py to **src/main/python** and overwrite the existing file.

Move all the files in the same directory.

`fbs run`

> 5th Step

Create the .exe

`fbs freeze`

> 6th Step

Crete the installer

`fbs installer`