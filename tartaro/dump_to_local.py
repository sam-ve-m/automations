from pymongo import MongoClient, errors

from src.utils.env_config import config

poseidon_mongo_connection = MongoClient(config("MONGO_CONNECTION_URL"))
local = MongoClient("mongodb://localhost:27018/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")

data_base = poseidon_mongo_connection["poseidon_raw_data"]
local_data_base = local["poseidon_raw_data"]

data_base_collections = data_base.list_collection_names()
local_data_base_collections = local_data_base.list_collection_names()

collections_names = set(data_base_collections)
collections_names -= set(local_data_base_collections) | {"system.views", "news_refinitiv"}

for collection in collections_names:
    print(f"Starting {collection}")
    poseidon_collection = data_base[collection]
    poseidon_cursor = poseidon_collection.find({})
    if poseidon_data := [x for x in poseidon_cursor]:
        local_collection = local_data_base[collection]
        local_collection.insert_many(poseidon_data)
