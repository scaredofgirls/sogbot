"""A data storage module for shelving data"""
import shelve
import logging

logger = logging.getLogger('sogbot')

default_config = {
    "storage": {
        "shelve": {
            "db_path": "/tmp/disc_bot.db"
        }
    }
}


class Storage():
    """An interface for storage"""
    def __init__(self, config=default_config):
        logger.debug("In shelve storage __init__")
        logger.debug("Using path: %s", config['storage']['shelve']['db_path'])
        self.path = config['storage']['shelve']['db_path']
        self.db = shelve.open(self.path, flag='c', writeback=False)

    def get_full_key(self, app, key):
        """idk"""
        return f"{app}::{key}"

    def read(self, app, key):
        """Read from storage"""
        logger.debug("Reading key '%s' for app '%s' from storage", key, app)
        fk = self.get_full_key(app, key)
        try:
            value = self.db[fk]
        except KeyError:
            value = None
        return value

    def write(self, app, key, value):
        """Write to storage"""
        logger.debug("Writing value '%s' to key '%s' for app '%s'"
                     "to storage", value, key, app)
        fk = self.get_full_key(app, key)
        try:
            self.db[fk] = value
        except Exception as e:
            logger.error(e)
            return False
        return True

    def delete(self, app, key):
        """Delete a record from storage"""
        logger.debug("Deleting key '%s' for app '%s' from storage", key, app)
        fk = self.get_full_key(app, key)
        try:
            del self.db[fk]
        except KeyError:
            return False
        return True

    def search(self, app, query):
        """Search the data store"""
        return ""
