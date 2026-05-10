"""A module for utilities that may be useful bot-wide"""
import yaml


def get_config(file_name="config.yaml"):
    """Read our configuration data form a file and return it
    as a dict"""
    with open(file_name, 'r', encoding='utf-8') as fd:
        y = yaml.safe_load(fd)
    return y


def do_guild_rollout(bot_config, extension_name, command):
    """A helper for setting up guild rollouts for commands
    Every extension should call this in __init__"""
    if len(bot_config['bot']['extensions'][extension_name]) == 0:
        return True
    for gid in bot_config['bot']['extensions'][extension_name]:
        command.add_guild_rollout(gid)
    return True
