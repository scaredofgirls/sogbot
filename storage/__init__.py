"""A module for managing storage for a nextcord
based bot"""
import importlib
import logging

logger = logging.getLogger('sogbot')
# Spec:
# all of the following return just the value
# read("app", "key")
# search("app", "query")?
# returns true or false to indicate success
# delete("app", "key")
# write("app", "key")


def init_storage(backend="shelve", config=None):
    """Initialize storage for the bot"""
    try:
        be_module = importlib.import_module(f"storage.{backend}")
    except Exception as e:
        logger.error(e)
    return be_module.Storage(config)
