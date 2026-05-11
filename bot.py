#!/usr/bin/env python3
"""A general purpose discord bot"""

import logging
import sys
from logging.handlers import RotatingFileHandler

import nextcord
from nextcord.ext import commands

import botutil
import storage

# Logging Config
log_fmt = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

bot_log = logging.getLogger("sogbot")
bot_log.setLevel(logging.DEBUG)
bot_log_handler = logging.StreamHandler(sys.stdout)
bot_log_handler.setFormatter(log_fmt)
bot_log.addHandler(bot_log_handler)

disc_log = logging.getLogger("nextcord")
disc_log.setLevel(logging.INFO)
disc_log_handler = RotatingFileHandler(
    "discord.log", maxBytes=104857600, backupCount=2
)
disc_log_handler.setFormatter(log_fmt)
disc_log.addHandler(disc_log_handler)
# Logging Config

bot_intents = nextcord.Intents.default()
bot_intents.message_content = True

bconf = botutil.get_config()
bot_log.setLevel(bconf["bot"]["log_level"])
st = storage.init_storage(config=bconf)

DISCORD_TOKEN = bconf["discord"]["bot_token"]

if __name__ == "__main__":
    bot_log.info("Starting up")
    bot = commands.Bot(
        command_prefix="!",
        intents=bot_intents,
        default_guild_ids=bconf["bot"]["default_guild_ids"],
    )
    setattr(bot, "storage", st)

    try:
        if len(bconf["bot"]["owner_ids"]) > 1:
            bot.owner_ids = set(bconf["bot"]["owner_ids"])
            bot_log.debug("Set owner_ids to %s", bot.owner_ids)
        else:
            bot.owner_id = bconf["bot"]["owner_ids"][0]
            bot_log.debug("Set owner_id to %s", bot.owner_id)
    except KeyError:
        bot_log.warning("Bot owner not defined.")
        bot_log.warning("Falling back on default owner detection.")

    @bot.event
    async def on_ready():
        """Routines to run once we're connected and ready to do bot things"""
        bot_log.info("Bot ready")
        bot_log.debug("%s connected to %s", bot.user.name, bot.guilds)

    @bot.command()
    async def eatpizza(ctx):
        """Responds with a pizza emote. Sort of a 'ping' function"""
        await ctx.send("\N{SLICE OF PIZZA}")

    for extension in bconf["bot"]["extensions"].items():
        bot.load_extension(extension)

    bot.run(DISCORD_TOKEN)
