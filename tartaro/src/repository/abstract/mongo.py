from abc import ABC
from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor
from pymongo.cursor import Cursor


class AbstractMongoCRUDRepository(ABC):
    collection: AsyncIOMotorCollection

    async def aggregate(self, pipeline: List[dict]) -> AsyncIOMotorCursor:
        async_cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
        return async_cursor

    async def find_all(self, query: dict = {}) -> Cursor:
        async_cursor = self.collection.find(query)
        query_result = await async_cursor.to_list(None)
        return query_result

    async def find_one(self, query: dict, project: dict = {}) -> dict:
        query_result = await self.collection.find_one(query, project)
        return query_result

    async def update_one(self, document_id: str, update: dict) -> bool:
        updates_made = await self.collection.update_one({"_id": document_id}, {'$set': update})
        was_something_updated = updates_made.modified_count > 0
        return was_something_updated
