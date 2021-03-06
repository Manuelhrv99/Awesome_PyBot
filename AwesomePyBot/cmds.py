from time import time
import economy
import games
import misc
import mod

PREFIX = "!"

class Cmd(object):
    def __init__(self, callables, func, cooldown=0):
        self.callables = callables
        self.func = func
        self.colldown = cooldown
        self.next_use = time()

cmds = [
    #Misc
    Cmd(["hello", "hi", "hey"], misc.hello, cooldown=15),
    Cmd(["about"], misc.about),
    Cmd(["uptime"], misc.uptime),
    Cmd(["userinfo", "ui"], misc.userinfo),
    Cmd(["shutdown"], misc.shutdown),
    #Economy
    Cmd(["coins", "money"], economy.coins),
    #Games
    Cmd(["coinflip", "flip"], games.coinflip, cooldown = 60),
    Cmd(["heist"], games.start_heist, cooldown = 60),
    #Moderation
    Cmd(["warn"], mod.warn),
    Cmd(["unwarn", "rmwarn"], mod.remove_warn)
]

def process(bot, user, message):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform(bot, user, cmd, *args)

def perform(bot, user, call, *args):
    if call in ("help", "commands", "cmds"):
        misc.help(bot, PREFIX, cmds)
    else:
        for cmd in cmds:
            if call in cmd.callables:
                if time() > cmd.next_use:
                    cmd.func(bot, user, *args)
                    cmd.next_use = time() + cmd.colldown
                else:
                    bot.send_message(f"Cooldown still in effect. Try again in {cmd.next_use - time():,.0f} seconds.")
                return
        bot.send_message(f"{user['name']}, \"{call}\" ins't a registered command.")