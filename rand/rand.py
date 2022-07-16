#!/usr/bin/env python3

from nextcord.ext import commands
from nextcord import SlashOption, Interaction
import nextcord
import logging
import random

logger = logging.getLogger('sogbot')


class rand(commands.Cog):
    def __init__(self, bot):
        self.app = "rand"
        self.bot = bot
        for gid in bot.config['bot']['guild_ids']:
            self.rand.add_guild_rollout(gid)

    @nextcord.slash_command(name="rand", description="Generate random numbers")
    async def rand(self, interaction: Interaction,
                   floor: int = SlashOption(description="lowest number",
                                            required=True),
                   ceiling: int = SlashOption(description="highest number",
                                              required=True),
                   count: int = SlashOption(description="Amount of numbers",
                                            required=True)):
        results = []
        while len(results) < count:
            this_int = random.randint(floor, ceiling)
            if this_int not in results:
                results.append(this_int)
        results.sort()
        message = ', '.join([str(r) for r in results])
        summed = sum(results)
        message = f"{message}\nThe sum of which is: {summed}"
        await interaction.response.send_message(message)


def setup(bot):
    bot.add_cog(rand(bot))


def teardown(bot):
    pass
