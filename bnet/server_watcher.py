#!/usr/bin/env python3

from nextcord.ext import commands, tasks
import requests
import logging
import json
import time

logger = logging.getLogger('sogbot')


class battleNet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watched_realm = None
        self.watched_realm_ctx = None
        self.last_realm_status = None
        self.bn_client = bot.config['bnet']['client_id']
        self.bn_secret = bot.config['bnet']['client_secret']
        self.wow_uri_base = bot.config['bnet']['uri_base']
        self.bnet_oauth_url = "https://us.battle.net/oauth/token"
        self.oauth_file = ".bnet_auth"
        self.oauth = None

        self.get_bn_auth_token()

    @commands.group()
    async def bnet(self, ctx):
        pass

    def oauth_from_file(self):
        with open(self.oauth_file, 'r') as fd:
            oauth_j = json.load(fd)
        self.oauth = oauth_j

    def oauth_to_file(self, oauth_j):
        with open(self.oauth_file, 'w') as fd:
            json.dump(oauth_j, fd)

    def get_bn_auth_token(self):
        if self.oauth is None:
            self.oauth_from_file()

        if self.oauth['expires'] > time.time():
            return

        data = {"grant_type": "client_credentials"}
        res = requests.post(self.bnet_oauth_url, data=data,
                            auth=(self.bn_client, self.bn_secret))
        res_j = res.json()
        res_j['expires'] = time.time() + res_j['expires_in']
        self.oauth = res_j
        self.oauth_to_file(res_j)

    def get_all_realm_ids(self):
        logger.debug('Getting realm ids')
        ids = []
        headers = {"Authorization": f"Bearer {self.oauth['access_token']}"}
        URI = "connected-realm/index?namespace=dynamic-classic-us"
        URL = f"{self.wow_uri_base}/{URI}"
        res = requests.get(URL, headers=headers)
        if res.status_code != 200:
            logger.debug(f'Status code was {res.status_code}')
            logger.debug('Returning "None"')
            return None

        j = res.json()
        for realm in j['connected_realms']:
            ids.append(realm['href'].split("/")[-1].split('?')[0])

        return ids

    def get_realm(self, realm_id):
        logger.debug(f"Looking for realm id: {realm_id}")
        URI = f"connected-realm/{realm_id}?namespace=dynamic-classic-us"
        URI = f"{URI}&locale=en_US"
        URL = f"{self.wow_uri_base}/{URI}"

        headers = {"Authorization": f"Bearer {self.oauth['access_token']}"}
        res = requests.get(URL, headers=headers)
        if res.status_code != 200:
            logger.debug(f"Status code was {res.status_code}")
            return None

        return res.json()

    def find_realm(self, realm_ids, realm_to_find):
        logger.debug(f"Searching for {realm_to_find}")
        for rid in realm_ids:
            realm = self.get_realm(rid)
            if realm is None:
                continue
            realm_name = realm['realms'][0]['name']
            if realm_name == realm_to_find:
                logger.info(f"Found Realm {realm_to_find}!")
                logger.info(f"Realm is currently: {realm['status']['name']}!")
                return realm['status']['name']
            else:
                logger.debug(f"Got name {realm_name} for id {rid}")

    def get_realm_status(self, realm):
        realm_ids = self.get_all_realm_ids()
        if realm_ids is None:
            logger.error("Could not retrieve list of realms :(")
            return None

        realm_status = self.find_realm(realm_ids, realm)
        return realm_status

    @bnet.command(name='rs', usage='RealmName',
                  brief='Shows the status of a WoW Classic Realm',
                  help="""This command queries the Battle.NET API for the
                  status of the specified WoW Classic Realm and returns it
                  to chat""")
    async def fetch_realm_status(self, ctx, realm):
        realm_ids = self.get_all_realm_ids()
        if realm_ids is None:
            logger.error("Could not retrieve list of realms :(")
            return None

        realm_status = self.find_realm(realm_ids, realm)
        response = f"The realm {realm} is currently {realm_status}"
        await ctx.send(response)

    @bnet.command(name='rw', usage='RealmName',
                  brief='Watch the status of a WoW Classic Realm',
                  help="""This command queries the Battle.NET API for the
                  status of the specified WoW Classic Realm and returns it
                  to chat if it changed""")
    async def watch_realm(self, ctx, realm):
        if self.watched_realm is not None:
            resp = f"I am already watching {self.watched_realm}"
            resp = f"{resp} in {ctx.channel.name} on {ctx.guild.name}"
            await ctx.send(resp)
            return
        self.watched_realm = realm
        self.watched_realm_ctx = ctx
        self.watcher.start()
        await ctx.send(f"Now watching the status of realm {realm}")

    @bnet.command(name='ru',
                  brief='Stop watching the status of a WoW Classic Realm',
                  help="""This command stops the querying of the Battle.NET
                  API for the status of the previously specified WoW
                  Classic Realm""")
    async def unwatch_realm(self, ctx):
        resp = f"Stopped watching status of realm {self.watched_realm}"
        self.watched_realm = None
        self.watcher.stop()
        await ctx.send(resp)

    @tasks.loop(seconds=300)
    async def watcher(self):
        logger.debug("watcher task checking realm status")
        this_status = self.get_realm_status(self.watched_realm)
        if this_status != self.last_realm_status:
            word = "currently" if self.last_realm_status is None else "now"
            response = f"Realm {self.watched_realm} is {word} {this_status}"
            await self.watched_realm_ctx.send(response)
        self.last_realm_status = this_status

    @watcher.before_loop
    async def before_watcher(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(battleNet(bot))


def teardown(bot):
    pass
