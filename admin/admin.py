from nextcord.ext import commands
import logging

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
        logger.debug(f"Trying to load module '{module}'")
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        logger.debug(f"Trying to unload module '{module}'")
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        logger.debug(f"Trying to reload module '{module}'")
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Admin(bot))
