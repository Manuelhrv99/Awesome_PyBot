# awesomePyBot

## Create .exe with pyinstaller

> 1st Step

Open a command prompt in your **AwesomePyBot_GUI** directory and execute the following:

`pyi-makespec main.py`

> 2nd Step

Inside the new **main.spec** file modify datas.

`datas=[ ('./files/*.db', 'resources'), ('./files/*.sql', 'resources') ],`

> 3rd Step

Run pyinstaller command.

`pyinstaller main.spec`