import logging

import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connection(table_name=None):
    logging.debug(f"Attempting to connect to MongoDB, table: {table_name}")
    uri = "mongodb+srv://tudolin:Rafinha2346@database.hvtbw.mongodb.net/?retryWrites=true&w=majority&appName=database"

    try:
        client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        data_base = client['database']
        client.admin.command('ping')
        logging.debug("Pinged MongoDB deployment successfully.")
        if table_name:
            collection = data_base[table_name]
            return collection
        return data_base
    except Exception as e:
        logging.error(f"An error occurred while connecting to the database: {e}")
        return None