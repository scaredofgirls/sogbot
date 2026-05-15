"""A nextcord module for generating random numbers"""

import logging
import random
from nextcord.ext import commands
from nextcord import SlashOption, Interaction
import nextcord
import botutil

logger = logging.getLogger("sogbot")


class Rand(commands.Cog):
    """Generate a random number"""

    def __init__(self, bot):
        self.app = "rand"
        self.bot = bot
        botutil.do_guild_rollout(
            bot.config, __name__, self.rand, [g.id for g in bot.guilds]
        )

    @nextcord.slash_command(name="rand", description="Generate random numbers")
    async def rand(
        self,
        interaction: Interaction,
        floor: int = SlashOption(description="lowest number", required=True),
        ceiling: int = SlashOption(
            description="highest number", required=True
        ),
        count: int = SlashOption(
            description="Amount of numbers", required=True
        ),
    ):
        """Generate a random number"""
        results = []
        while len(results) < count:
            this_int = random.randint(floor, ceiling)
            if this_int not in results:
                results.append(this_int)
        results.sort()
        message = ", ".join([str(r) for r in results])
        summed = sum(results)
        message = f"{message}\nThe sum of which is: {summed}"
        await interaction.response.send_message(message)


def setup(bot):
    """Code to run at extension load time"""
    bot.add_cog(Rand(bot))


def teardown(bot):
    """Code to run at extension unload time"""
    return
