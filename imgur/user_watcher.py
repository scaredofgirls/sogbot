#!/usr/bin/env python3

from nextcord.ext import commands, tasks
import nextcord
import requests
import logging
import time
import datetime

# users should be:
"""
{
    "newest_ts" = 0,
    "notify_channels": ["guild_id:channel_id", "guild_id:channel_id"]
}
"""
logger = logging.getLogger('sogbot')


class imgurAPI(commands.Cog):
    def __init__(self, bot):
        self.app = "imgurwatcher"
        self.bot = bot
        self._setup_http(bot.config['imgur']['client_id'],
                         bot.config['imgur']['client_secret'],
                         bot.config['imgur']['api']['base'],
                         bot.config['imgur']['api']['subs'])
        for gid in bot.config['bot']['guild_ids']:
            self.imgur.add_guild_rollout(gid)
        self._load_users()  # Loads from storage into self.watched_users
        self._start_watching()

    @nextcord.slash_command()
    async def imgur(self, name="imgur"):
        pass

    @imgur.subcommand(name="stop",
                      description="""Stop checking imgur for posts from
                      watched users""")
    async def stop(self, interaction: nextcord.Interaction):
        """TODO: make this do the thing it says it does instead
        of this placeholder
        """
        await interaction.response.send_message(self.watched_users)

    @imgur.subcommand(name='status',
                      description="""Shows the config for the imgur
                      functionality of this bot""")
    @commands.is_owner()
    async def status(self, interaction: nextcord.Interaction):
        resp = "Watching the following users:"
        this_embed = nextcord.Embed(colour=0x00FFFF,
                                    description=resp,
                                    title="User Watcher Status", type="rich",
                                    timestamp=datetime.datetime.now())
        for usr in self.watched_users:
            last_up = datetime.datetime.fromtimestamp(
                self.watched_users[usr]['newest_ts']
            )
            last_up = last_up.strftime('%c')
            details = f"Last Update: {last_up}\n"
            details = f"{details} Notifying Channels:"
            for nch in self.watched_users[usr]['notify_channels']:
                g, c = nch.split(':')
                this_guild = self.bot.get_guild(int(g))
                gname = this_guild.name
                chan = this_guild.get_channel(int(c)).name
                details = f"{details} {gname}: #{chan}"
            this_embed.add_field(name=usr, value=details)
        this_embed.add_field(name="Watcher running",
                             value=f"{self.watcher.is_running()}")
        await interaction.response.send_message(embed=this_embed)

    @imgur.subcommand(name='watch_user',
                      description="""Periodically query imgur for new posts
                      from a user""")
    async def watch_user(self, interaction: nextcord.Interaction, user: str):
        notify_channel = f"{interaction.guild_id}:{interaction.channel_id}"

        if user in self.watched_users:
            if notify_channel in self.watched_users[user]["notify_channels"]:
                out = f"Already watching {user} and notifying this channel"
                await interaction.response.send_message(out)
                return
            self._update_user(user, notify_channel)
            resp = f"This channel will now get notifications about {user}"
            await interaction.response.send_message(resp)
            return

        self._add_new_user(user, notify_channel)
        await interaction.response.send_message(f"Now watching user {user}")

    @imgur.subcommand(name='unwatch_user',
                      description="""Stops the querying of the imgur API for
                      new posts from the specified user""")
    async def unwatch_user(self, interaction: nextcord.Interaction, user: str):
        if user not in self.watched_users:
            resp = f"Not watching {user}"
            await interaction.response.send_message(resp)
            return

        del self.watched_users[user]
        self._update_storage()
        resp = f"No longer watching {user} from any channels"
        await interaction.response.send_message(resp)

    @tasks.loop(seconds=14400)
    async def watcher(self):
        logger.debug("in watcher task")
        for user in self.watched_users:
            try:
                response = self._check_submissions(user)
            except nextcord.errors.HTTPException as e:
                logger.error("Exception in watcher calling _check_submissions")
                logger.error("%s", e)
                return
            if response is None:
                logger.debug("Got None from _check_submissions. ending iter")
                logger.debug("Resting, for the imgur API is a fragile thing.")
                time.sleep(10)
                continue
            for nc in self.watched_users[user]["notify_channels"]:
                chan_id = int(nc.split(":")[1])
                channel = self.bot.get_channel(chan_id)
                try:
                    if len(response) >= 2000:
                        response = response[:1998]
                    await channel.send(response)
                except nextcord.errors.HTTPException as e:
                    logger.error("Exception in watcher sending result to chan")
                    logger.error("%s", e)
                    return
            logger.debug("Resting, for the imgur API is a fragile thing.")
            time.sleep(10)

    @watcher.before_loop
    async def before_watcher(self):
        await self.bot.wait_until_ready()

    # Start private methods
    def _start_watching(self):
        logger.debug("Starting imgur watcher")
        self.watcher.start()

    def _stop_watching(self):
        logger.debug("Stopping imgur watcher")
        self.watcher.stop()

    def _load_users(self):
        self.watched_users = self.bot.storage.read(self.app, "watched_users")
        if self.watched_users is None:
            self.watched_users = {}

    def _setup_http(self, client_id, client_secret,
                    api_base, api_subs):
        self.http_headers = {"Authorization": f"Client-ID {client_id}"}
        self.url_pattern = f"{api_base}/{api_subs}"

    def _check_submissions(self, user):
        logger.debug(f"checking profile of {user} for new posts")
        response = None

        threshold = int(time.time()) - 43200  # 12 hours ago
        if self.watched_users[user]['newest_ts'] > threshold:
            logger.debug(f"Newest post from {user} found recently.")
            logger.debug(f"Not checking for new post from {user}.")
            return response

        submission_info = self._get_new_user_submission(user)
        # If the success key is present, _get_new_user_submission returned
        # the whole response object and not just the most recent post. This
        # indicates an error
        if 'success' not in submission_info:
            if (submission_info['datetime'] >
                    self.watched_users[user]['newest_ts']):
                st = time.localtime(submission_info['datetime'])
                sub_date = time.strftime("%H:%M:%S %Z on %A, %B %d %Y", st)
                logger.debug(f"New post from {user} found!")
                response = f"New post from {user} found!\n"
                response = f"{response}The post was made at {sub_date}\n"
                response = f"{response}{submission_info['link']}"
                self.watched_users[user]['newest_ts'] = (
                    submission_info['datetime']
                )
                self._update_storage()
            else:
                logger.info(f"No new images found for {user}")
        else:
            response = f"Received error while fetching info for '{user}'."
            response = f"{response}\n```{submission_info}```"
        return response

    def _update_storage(self):
        if self.bot.storage.write(self.app, "watched_users",
                                  self.watched_users):
            pass
        else:
            logger.error("Got False from storate.write()")

    def _get_new_user_submission(self, user):
        this_url = self.url_pattern.format(user)
        logger.debug(f"in _get_new_user_submission with url {this_url}")
        res = requests.get(this_url, headers=self.http_headers)
        j = res.json()
        logger.debug(f"got json {j}")
        logger.debug(f"got headers: {res.headers}")
        if j['success']:
            logger.debug("success evaluates True, returning json['data'][0]")
            return j['data'][0]
        else:
            logger.debug("success evalutes False, returning whole object")
            return j

    def _update_user(self, user, notify_channel):
        if notify_channel not in self.watched_users[user]["notify_channels"]:
            self.watched_users[user]["notify_channels"].append(notify_channel)
            self._update_storage()

    def _add_new_user(self, user, notify_channel):
        user_data = {
            "newest_ts": 0, "notify_channels": [notify_channel]
        }
        self.watched_users[user] = user_data
        self._update_storage()


def setup(bot):
    bot.add_cog(imgurAPI(bot))


def teardown(bot):
    # We should call _stop_watching() here, it seems like the task might
    # not be killed when we reload the cog. Can we access methods of the cog
    # from the bot object, given we call add_cog()?
    pass
