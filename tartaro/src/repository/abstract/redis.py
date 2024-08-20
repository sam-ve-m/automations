from abc import ABC
from typing import Optional

from aioredis.client import Redis
import orjson

from src.core.dto.graph import GraphSample


class AbstractRedisCRUDRepository(ABC):
    cache_connection: Redis
    dump_methods = {
        bytes: lambda x: x,
        GraphSample: lambda x: orjson.dumps(x.dict())
    }

    async def get(self, key: str) -> Optional[dict]:
        if value := await self.cache_connection.get(key):
            try:
                value = orjson.loads(value)
            except orjson.JSONDecodeError:
                pass
        return value

    async def set(self, key: str, value: dict, ttl: int = None) -> bool:
        dump_method = self.dump_methods.get(type(value), orjson.dumps)
        bytes_value = dump_method(value)
        return await self.cache_connection.set(key, bytes_value, ex=ttl)

    async def delete(self, key: str) -> bool:
        return await self.cache_connection.delete(key) > 0
