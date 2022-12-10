#!/usr/bin/env python3

from nextcord.ext import commands
import nextcord
import logging
import requests
from bs4 import BeautifulSoup
import datetime

logger = logging.getLogger('sogbot')
cog_desc = "Commands for interaction with a Islands of Myth"


class iom(commands.Cog):
    def __init__(self, bot):
        self.app = "iom"
        self.bot = bot
        self.mud = {
            "host": bot.config['mud']['host'],
            "cgi_uri": bot.config['mud']['cgi_uri']
        }
        for gid in bot.config['bot']['guild_ids']:
            self.iom.add_guild_rollout(gid)

    @nextcord.slash_command(name="iom",
                            description=cog_desc)
    async def iom(self, name="iom"):
        pass

    @iom.subcommand(name="who",
                    description="See who is playing!")
    async def who(self, interaction: nextcord.Interaction):
        resp = self._do_mud_command("who")

        this_embed = nextcord.Embed(colour=0x145DA0,
                                    description="Players Currently Online:",
                                    title="IoM 'who'", type="rich",
                                    timestamp=datetime.datetime.now())
        for player in resp:
            this_value = f"Level {player[3]} {player[1].title()}"
            this_value = f"{this_value} {player[2].title()}"
            this_embed.add_field(name=player[0].title(), value=this_value)
        await interaction.response.send_message(embed=this_embed)

    @iom.subcommand(name="finger",
                    description="Finger a player.")
    async def finger(self, interaction: nextcord.Interaction, player: str):
        resp = self._do_mud_command("finger", player)
        await interaction.response.send_message(resp)

    def _do_mud_command(self, command, args=None):
        if command == "who":
            resp = self._get_who_cgi()
        if command == "finger":
            resp = self._get_finger_cgi(args)
        return resp

    def _do_cgi_req(self, uri, args=None):
        url = f"http://{self.mud['host']}/{self.mud['cgi_uri']}/{uri}"
        if args is not None:
            url = f"{url}?{args}"
        r = requests.get(url)
        return r.text

    def _get_finger_cgi(self, player):
        q_args = f"name={player}&format=flat"
        finger_info = ">>> "
        finger_info += self._do_cgi_req("korth.c", q_args)
        return finger_info

    def _get_who_cgi(self):
        users_on = []
        who_html = self._do_cgi_req("who.c")
        soup = BeautifulSoup(who_html, 'html.parser')
        for user in soup.ol.find_all('li'):
            bits = user.get_text().split()

            users_on.append((bits[0], bits[2].rstrip(','), bits[5],
                             bits[8].rstrip('.')))
        return users_on


def setup(bot):
    bot.add_cog(iom(bot))


def teardown(bot):
    pass
