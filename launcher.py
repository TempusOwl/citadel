# You must create file called token.0 with your token number only (check for whitespaces) like: /lib/bot/token.0
# Project Link https://github.com/TempusOwl/Praetorian Read README requirements before starting.
# Startup errors? Likely means you are missing dependencies read the line above.
# Intents must be enabled via Discord API Dashboard or you may encounter errors.
# When ready run this file using python listed on github.

from lib.bot import bot

VERSION = "0.1.3a"

bot.run(VERSION)
