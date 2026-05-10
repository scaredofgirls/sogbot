#!/usr/bin/env python3
"""Discord interactions for sending commands to a minecraft server"""

import logging
from mcrcon import MCRcon  # type: ignore[import-untyped]
from nextcord.ext import commands
from nextcord import SlashOption
import nextcord
import botutil

logger = logging.getLogger('sogbot')
COG_DESC = "Commands for interaction with a Minecraft RCON server"
# this_mod_servers = [1121191247827185664, 285906403477159936]


class Mcrcon(commands.Cog):
    """Interact with the Minecraft mcrcon service"""
    def __init__(self, bot, bot_config):
        self.app = "mcrcon"
        self.bot = bot
        self.bot_config = bot_config
        self.rcon = {
            "host": bot_config['mc']['rcon']['host'],
            "password": bot_config['mc']['rcon']['pass']
        }
        botutil.do_guild_rollout(bot_config, __name__, self.mc)

    @nextcord.slash_command(name="mc", description=COG_DESC)
    async def mc(self, name="mc"):
        """A place holder to get the base command created"""

    @mc.subcommand(name="info",
                   description="Show the modpack and server currently in use")
    async def info(self, interaction: nextcord.Interaction):
        """Show some info about our current minecraft setup"""
        server = self.bot_config['mc']['info']['server']
        modpack = self.bot_config['mc']['info']['modpack']
        msg = f"Now running {modpack} on {server}"
        await interaction.response.send_message(msg)

    @mc.subcommand(name="say",
                   description="Send a message to Minecraft chat!")
    async def say(self, interaction: nextcord.Interaction,
                  words: str = SlashOption(description="Message to send",
                                           required=True)):
        """Send a message to Minecraft chat"""
        self._do_rcon_command(f"/say {interaction.user.display_name}: {words}")
        resp = "Message sent!"
        await interaction.response.send_message(resp)

    @mc.subcommand(name="who",
                   description="See who is currently online")
    async def who(self, interaction: nextcord.Interaction):
        """See who is currently online"""
        resp = self._do_rcon_command("/list")
        await interaction.response.send_message(resp)

    @mc.subcommand(name="whitelist", description="Manage the MC whitelist")
    async def whitelist(self, interaction: nextcord.Interaction):
        """Manage the MC whitelist"""
        return

    @whitelist.subcommand(name="list", description="View the MC whitelist")
    async def wl_list(self, interaction: nextcord.Interaction):
        """View the whitelist"""
        resp = self._do_rcon_command("/whitelist list")
        await interaction.response.send_message(resp)

    @whitelist.subcommand(name="add",
                          description="Add a user to the whitelist")
    async def wl_add(self, interaction: nextcord.Interaction,
                     user: str = SlashOption(
                         description="Minecraft username to whitelist",
                         required=True)):
        """Add a user to the whitelist"""
        resp = self._do_rcon_command(f"/whitelist add {user}")
        await interaction.response.send_message(resp)

    @whitelist.subcommand(name="remove",
                          description="Remove a user from the whitelist")
    async def wl_rm(self, interaction: nextcord.Interaction,
                    user: str = SlashOption(description="User to de-whitelist",
                                            required=True)):
        """Remove a user from the whitelist"""
        resp = self._do_rcon_command(f"/whitelist remove {user}")
        await interaction.response.send_message(resp)

    def _do_rcon_command(self, command):
        try:
            with MCRcon(self.rcon['host'], self.rcon['password']) as mcr:
                resp = mcr.command(command)
        except ConnectionRefusedError:
            resp = f"Connection to {self.rcon['host']} was refused"
        return resp


def setup(bot, bot_config):
    """Code to run at extension load time"""
    bot.add_cog(Mcrcon(bot, bot_config))


def teardown(bot):
    """Dummy function for handling graceful shutdown"""
    return
