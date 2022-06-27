#!/usr/bin/env python3

import logging
import botutil
from logging.handlers import RotatingFileHandler
import sys
import storage
from nextcord.ext import commands
import nextcord

# Logging Config
log_fmt = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

bot_log = logging.getLogger('sogbot')
bot_log.setLevel(logging.DEBUG)
bot_log_handler = logging.StreamHandler(sys.stdout)
bot_log_handler.setFormatter(log_fmt)
bot_log.addHandler(bot_log_handler)

disc_log = logging.getLogger('nextcord')
disc_log.setLevel(logging.INFO)
disc_log_handler = RotatingFileHandler("discord.log", maxBytes=104857600,
                                       backupCount=2)
disc_log_handler.setFormatter(log_fmt)
disc_log.addHandler(disc_log_handler)
# Logging Config

bot_intents = nextcord.Intents.default()
bot_intents.message_content = True

bot_config = botutil.get_config()
st = storage.init_storage(config=bot_config)

DISCORD_TOKEN = bot_config['discord']['bot_token']

if __name__ == '__main__':
    bot_log.info("Starting up")
    bot = commands.Bot(command_prefix='!', intents=bot_intents)
    bot.config = bot_config
    bot.storage = st

    try:
        if len(bot_config['bot']['owner_ids']) > 1:
            bot.owner_ids = set(bot_config['bot']['owner_ids'])
            bot_log.debug(f"Set owner_ids to {bot.owner_ids}")
        else:
            bot.owner_id = bot_config['bot']['owner_ids'][0]
            bot_log.debug(f"Set owner_id to {bot.owner_id}")
    except KeyError:
        bot_log.warning("Bot owner not defined.")
        bot_log.warning("Falling back on default owner detection.")

    @bot.event
    async def on_ready():
        bot_log.info("Bot ready")
        bot_log.debug(f"{bot.user.name} connected to {bot.guilds}")

    @bot.command()
    async def eatpizza(ctx):
        await ctx.send('\N{SLICE OF PIZZA}')

    extensions = [
        # 'BNet.server_watcher'
        'admin.admin', 'imgur.user_watcher', 'mc.mcrcon',
        'rand.rand'
    ]
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            out = f"Failed to load extension {extension}\n{type(e).__name__}"
            out = f"{out}{e}"
            bot_log.error(out)

    bot.run(DISCORD_TOKEN)
