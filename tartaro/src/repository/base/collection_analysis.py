from pymongo.collection import Collection

from src.core.static.pipeline.count_mongo_keys import CountCollectionKeys
from src.repository.abstract.mongo import AbstractMongoCRUDRepository


class MongoCollectionRepository(AbstractMongoCRUDRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    async def missing_fields(self, filter_query: dict = {}) -> dict:
        keys_count = await self.aggregate([{"$match": filter_query}, *CountCollectionKeys.count_keys_pipeline])
        keys = {document.get("_id"): document.get("covered_items") async for document in keys_count}
        return keys

    async def find_ticker_by_id(self, ticker_id: str) -> dict:
        query = {"_id": ticker_id}
        project = {"news.raw_news": 0, "full_balance_sheet": 0, "street_events.raw_event": 0}
        ticker = await self.find_one(query, project)
        return ticker

    async def update_ticker(self, ticker_dict: dict) -> bool:
        ticker_id = ticker_dict.get("_id")
        return await self.update_one(ticker_id, ticker_dict)
