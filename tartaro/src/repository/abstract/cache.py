from functools import wraps
from typing import Optional, Callable

from aioredis.client import Redis

from src.repository.abstract.redis import AbstractRedisCRUDRepository


class AbstractCacheRepository(AbstractRedisCRUDRepository):
    cache_connection: Redis

    async def _get_cache(self, function_name: str) -> Optional[dict]:
        return await self.get(function_name)

    async def _save_cache(self, function_name: str, return_value: dict, ttl: int = None) -> bool:
        return await self.set(function_name, return_value, ttl)

    async def _clean_cache(self, function: Callable, *args, **kwargs) -> bool:
        key = ":".join((function.__name__, *map(str, args), *map(str, kwargs.values())))
        return await self.delete(key)


def _clean_value(raw_value):
    value = str(raw_value)
    value = value.replace(":", "-")
    value = value.replace("'", "")
    value = value.replace("{", "")
    value = value.replace("}", "")
    return value


def async_cached_operation(ttl_in_seconds: Optional[int] = None):

    def async_def_decorator(function):
        function_name = function.__name__

        @wraps(function)
        async def search_in_cache_before_executing_method(self: AbstractCacheRepository, *args, **kwargs):
            cache_key = ":".join((
                function_name,
                *map(_clean_value, args),
                *map(_clean_value, kwargs.values())
            ))
            if cache := await self._get_cache(cache_key):
                return cache
            function_return = await function(self, *args, **kwargs)
            await self._save_cache(cache_key, function_return, ttl_in_seconds)
            return function_return
        search_in_cache_before_executing_method.__name__ = function_name
        return search_in_cache_before_executing_method

    return async_def_decorator
