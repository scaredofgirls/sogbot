"""A module for utilities that may be useful bot-wide"""

import logging
import yaml

logger = logging.getLogger("sogbot")


def get_config(file_name="config.yaml"):
    """Read our configuration data form a file and return it
    as a dict"""
    with open(file_name, "r", encoding="utf-8") as fd:
        y = yaml.safe_load(fd)
    return y


def do_guild_rollout(bot_config, extension_name, command, all_guilds=None):
    """A helper for setting up guild rollouts for commands
    Every extension should call this in __init__"""
    load_all = len(bot_config["bot"]["extensions"][extension_name]) == 0
    if load_all and all_guilds is not None:
        guilds_to_join = all_guilds
    else:
        guilds_to_join = bot_config["bot"]["extensions"][extension_name]

    for gid in guilds_to_join:
        command.add_guild_rollout(gid)


def set_bot_owner(bot):
    """Determine the id for the owner of the bot"""
    try:
        if len(bot.config["bot"]["owner_ids"]) > 1:
            bot.owner_ids = set(bot.config["bot"]["owner_ids"])
            logger.debug("Set owner_ids to %s", bot.owner_ids)
        else:
            bot.owner_id = bot.config["bot"]["owner_ids"][0]
            logger.debug("Set owner_id to %s", bot.owner_id)
    except KeyError:
        logger.warning("Bot owner not defined.")
        logger.warning("Falling back on default owner detection.")
