import asyncio
from typing import Dict

from src.core.dto.graph import GraphSample
from src.core.static.pipeline.suply_excel import SupplyExcel
from src.repository.abstract.cache import AbstractCacheRepository, async_cached_operation
from src.repository.base.collection_analysis import MongoCollectionRepository
from src.utils.env_config import config


def all_collections(function):
    async def reproduce_in_all_collections(self, *args, **kwargs):
        collections_keys_coverage = {}
        for collection_name, collection_repository in self.collections.items():
            if keys_coverage := await function(collection_repository, *args, **kwargs):
                collections_keys_coverage.update({collection_name: keys_coverage})
        return collections_keys_coverage
    reproduce_in_all_collections.__name__ = function.__name__
    return reproduce_in_all_collections


class MongoDatabaseRepository(AbstractCacheRepository, MongoCollectionRepository):
    database_name = config("MONGO_DATABASE_ANALYSIS")

    def __init__(self, mongo_infrastructure, redis_infrastructure):
        self.cache_connection = redis_infrastructure
        database = mongo_infrastructure[self.database_name]
        loop = asyncio.get_event_loop()
        collections_names = loop.run_until_complete(database.list_collection_names())
        if "system.views" in collections_names:
            collections_names.remove("system.views")
        self.collections: Dict[str, MongoCollectionRepository] = {
            collection_name: MongoCollectionRepository(database[collection_name])
            for collection_name in collections_names
        }

    @async_cached_operation(ttl_in_seconds=600)
    @all_collections
    async def missing_fields(self) -> dict:
        return await self.missing_fields()

    @async_cached_operation(ttl_in_seconds=120)
    @all_collections
    async def find_ticker_by_id(self, ticker_id: str) -> dict:
        return await self.find_ticker_by_id(ticker_id)

    @async_cached_operation(ttl_in_seconds=600)
    async def missing_fields_in_filter(self, collection_name: str, filter_query: dict):
        mongo_query = {
            field: {"$exists": is_covered}
            for field, is_covered in filter_query.items()
        }
        collection_repository = self.collections.get(collection_name)
        if keys_coverage := await collection_repository.missing_fields(mongo_query):
            return keys_coverage
        return {"_id": []}

    async def update_ticker_collections(self, ticker_collections_update: dict) -> dict:
        collections_updates_status = {}
        for collection_name, ticker in ticker_collections_update.items():
            collection_repository = self.collections.get(collection_name)
            update_status = await collection_repository.update_ticker(ticker)
            collections_updates_status.update({collection_name: update_status})
        else:
            await self._clean_cache(self.find_ticker_by_id, ticker.get("_id"))
        return collections_updates_status

    @async_cached_operation(ttl_in_seconds=180)
    async def top_tickers_sample(self, collection: str, filter_query: dict, top_symbols: list) -> GraphSample:
        # filter_query.update({"_id:": {"$in": top_symbols}}) TODO: Enquanto não houver uma fonte para os top symbols
        filter_query.update({"$and": [{"_id": {"$not": {"$type": 7}}}]})
        distinct_keys_pipeline = [{"$match": filter_query}] + await SupplyExcel.get_distinct_keys_pipeline()
        collection_repository = self.collections.get(collection)
        distinct_keys = await collection_repository.aggregate(distinct_keys_pipeline)

        sample_possible_fields = [key.get("_id") async for key in distinct_keys]
        sample_possible_fields.sort()
        sample_tickers = await collection_repository.find_all(filter_query)
        return GraphSample(
            sample=sample_tickers,
            possible_fields=sample_possible_fields,
        )
