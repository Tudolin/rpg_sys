import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connection(table_name=None):
    uri = "mongodb+srv://tudolin:Rafinha2346@database.hvtbw.mongodb.net/?retryWrites=true&w=majority&appName=database"

    try:
        client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        data_base = client['database']
        if table_name:
            collection = data_base[table_name]
            return collection
        return data_base
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
