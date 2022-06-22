import sqlite3

SQL_CREATE_TABLE = """
CREATE TABLE {0}(
st_key text,
st_value blob,
PRIMARY KEY(st_key)
);
"""

SQL_TABLE_EXISTS = """
SELECT 1 FROM sqlite_master WHERE type='table' AND name='{0}'
"""

SQL_VALUE_FROM_KEY = """
SELECT
    st_value AS value
FROM
    {0}
WHERE
    st_key = {1}"""

SQL_VALUE_TO_KEY = "REPLACE INTO {0} (st_key, st_value) VALUES (?, ?)"


default_config = {
    "path": "/tmp/sqlite.db"
}


class Storage():
    def __init__(self, config=default_config):
        self.path = config['path']
        self.con = sqlite3.connect(self.path)
        self.curs = self.con.cursor()

    def _table_exists(self, table):
        self.curs.execute(SQL_TABLE_EXISTS)
        rows = self.curs.fetchall()
        if len(rows) > 0:
            return True
        return False

    def _create_table(self, table):
        "True on success, False on failure"
        query = SQL_CREATE_TABLE.format(table)
        self.curs.execute(query)
        if self._table_exists(table):
            return True
        else:
            return False

    def read(self, app, key):
        if not self._table_exists(app):
            self._create_table(app)
        query = SQL_VALUE_FROM_KEY.format(app, key)
        self.curs.execute(query)
        result = self.curs.fetchall()
        if len(result) > 0:
            return result[0]
        return None

    def write(self, app, key, value):
        "True on success, false on failure"
        if not self._table_exists(app):
            self._create_table(app)
        query = SQL_VALUE_TO_KEY.format(app)
        self.curs.execute(query, (key, value))
        if self.curs.lastrowid is not None:
            return True
        return False

    def search(self):
        pass
