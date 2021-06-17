# awesomePyBot

## Setup for the virtual environment

> 1st Step

Be sure to start in the correct folder.

Open a command prompt in your project directory and execute the following:

`%LOCALAPPDATA%\Programs\Python\Python36\python -m venv venv`

`call venv\Scripts\activate.bat`

> 2nd Step

Install the libraries.

`pip install fbs` 
`pip install PyQt5`
`pip install PySide6`
`pip install irc`
`pip install requests`
`pip install datetime`

> 3rd Step

Test that the app still works.

`python main.py`

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