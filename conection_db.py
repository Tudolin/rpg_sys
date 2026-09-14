import logging
import os
import sqlite3

from config import Config
from local_db import Collection

_conn = None

# Every "collection" the app uses. Declared up front so `connection()`
# without a table_name (the Database-like object) can expose them as
# attributes (db.chars, db.sessions, ...) the same way a pymongo Database did.
_COLLECTION_NAMES = ["users", "chars", "sessions", "classes", "races", "abilities", "enemies"]


class Database:
    def __init__(self, conn):
        self._collections = {name: Collection(conn, name) for name in _COLLECTION_NAMES}

    def __getattr__(self, name):
        try:
            return self._collections[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        return self._collections[name]


def _get_conn():
    global _conn
    if _conn is None:
        db_path = Config.DATABASE_PATH
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        _conn = sqlite3.connect(db_path, check_same_thread=False)
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=OFF")
    return _conn


def connection(table_name=None):
    try:
        conn = _get_conn()
        database = Database(conn)
        if table_name:
            return database[table_name]
        return database
    except Exception as e:
        logging.error("An error occurred while opening the local database: %s", e)
        return None
