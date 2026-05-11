"""Module for commands related to nextcord
bot administration"""
import logging
from nextcord.ext import commands

logger = logging.getLogger('sogbot')


class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        logger.info("Initializing admin cog")
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        logger.debug("Trying to load module '%s'", module)
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        logger.debug("Trying to unload module '%s'", module)
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        logger.debug("Trying to reload module '%s'", module)
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='speak', hidden=True)
    @commands.is_owner()
    async def speak(self, ctx, cid: int, words: str):
        """Says words in a chat"""
        chan = self.bot.get_channel(cid)
        await chan.send(words)


def setup(bot):
    """Called by nextcord when an extension is loaded"""
    bot.add_cog(Admin(bot))


def teardown(bot):
    """Called by nextcord when an extension is unloaded"""
    return
