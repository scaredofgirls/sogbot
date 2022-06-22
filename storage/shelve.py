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
    def __init__(self, config=default_config):
        logger.debug("In shelve storage __init__")
        logger.debug(f"Using path: {config['storage']['shelve']['db_path']}")
        self.path = config['storage']['shelve']['db_path']
        self.db = shelve.open(self.path, flag='c', writeback=False)

    def get_full_key(self, app, key):
        return f"{app}::{key}"

    def read(self, app, key):
        logger.debug(f"Reading key '{key}' for app '{app}' from storage")
        fk = self.get_full_key(app, key)
        try:
            value = self.db[fk]
        except KeyError:
            value = None
        return value

    def write(self, app, key, value):
        logger.debug(f"Writing value '{value}' to key '{key}' for app '{app}' "
                     "to storage")
        fk = self.get_full_key(app, key)
        try:
            self.db[fk] = value
        except Exception as e:
            logger.error(e)
            return False
        return True

    def delete(self, app, key):
        logger.debug(f"Deleting key '{key}' for app '{app}' from storage")
        fk = self.get_full_key(app, key)
        try:
            del self.db[fk]
        except KeyError:
            return False
        return True

    def search(self, app, query):
        return ""
