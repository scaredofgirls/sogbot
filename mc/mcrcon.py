#!/usr/bin/env python3
"""Discord interactions for sending commands to a minecraft server"""

import logging
from mcrcon import MCRcon
from nextcord.ext import commands
from nextcord import SlashOption
import nextcord

logger = logging.getLogger('sogbot')
COG_DESC = "Commands for interaction with a Minecraft RCON server"
this_mod_servers = [1121191247827185664, 285906403477159936]


class mcrcon(commands.Cog):
    def __init__(self, bot):
        self.app = "mcrcon"
        self.bot = bot
        self.rcon = {
            "host": bot.config['mc']['rcon']['host'],
            "password": bot.config['mc']['rcon']['pass']
        }
        # for gid in bot.config['bot']['guild_ids']:
        for gid in this_mod_servers:
            self.mc.add_guild_rollout(gid)

    @nextcord.slash_command(name="mc", description=COG_DESC,
                            guild_ids=this_mod_servers)
    async def mc(self, name="mc"):
        """A place holder to get the base command created"""

    @mc.subcommand(name="info",
                   description="Show the modpack and server currently in use")
    async def info(self, interaction: nextcord.Interaction):
        server = self.bot.config['mc']['info']['server']
        modpack = self.bot.config['mc']['info']['modpack']
        msg = f"Now running {modpack} on {server}"
        await interaction.response.send_message(msg)

    @mc.subcommand(name="say",
                   description="Send a message to Minecraft chat!")
    async def say(self, interaction: nextcord.Interaction,
                  words: str = SlashOption(description="Message to send",
                                           required=True)):
        self._do_rcon_command(f"/say {interaction.user.display_name}: {words}")
        resp = "Message sent!"
        await interaction.response.send_message(resp)

    @mc.subcommand(name="who",
                   description="See who is currently online")
    async def who(self, interaction: nextcord.Interaction):
        resp = self._do_rcon_command("/list")
        await interaction.response.send_message(resp)

    @mc.subcommand(name="whitelist", description="Manage the MC whitelist")
    async def whitelist(self, interaction: nextcord.Interaction):
        pass

    @whitelist.subcommand(name="list", description="View the MC whitelist")
    async def wl_list(self, interaction: nextcord.Interaction):
        resp = self._do_rcon_command("/whitelist list")
        await interaction.response.send_message(resp)

    @whitelist.subcommand(name="add",
                          description="Add a user to the whitelist")
    async def wl_add(self, interaction: nextcord.Interaction,
                     user: str = SlashOption(
                         description="Minecraft username to whitelist",
                         required=True)):
        resp = self._do_rcon_command(f"/whitelist add {user}")
        await interaction.response.send_message(resp)

    @whitelist.subcommand(name="remove",
                          description="Remove a user from the whitelist")
    async def wl_rm(self, interaction: nextcord.Interaction,
                    user: str = SlashOption(description="User to de-whitelist",
                                            required=True)):
        resp = self._do_rcon_command(f"/whitelist remove {user}")
        await interaction.response.send_message(resp)

    def _do_rcon_command(self, command):
        try:
            with MCRcon(self.rcon['host'], self.rcon['password']) as mcr:
                resp = mcr.command(command)
        except ConnectionRefusedError:
            resp = f"Connection to {self.rcon['host']} was refused"
        return resp


def setup(bot):
    bot.add_cog(mcrcon(bot))


def teardown(bot):
    pass
