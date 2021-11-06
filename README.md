# Awesome PyBot

## Create .exe with pyinstaller

> 1st Step

Open a command prompt in your **AwesomePyBot_GUI** directory and execute the following:

`pyi-makespec main.py`

> 2nd Step

Inside the new **main.spec** file modify datas.

`datas=[('./resources/database.db', 'resources'), ('./resources/script.sql', 'resources')],`

> 3rd Step

Run pyinstaller command.

`pyinstaller main.spec`

> 4th Step

Inside the new /dist/main/ folder, double click the AwesomePyBot.exe and voilà!
